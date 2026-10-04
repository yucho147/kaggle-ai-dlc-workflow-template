"""Explicit data modes and a strict, ID-aligned one-column submission contract."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from loguru import logger
from omegaconf import DictConfig
from sklearn.datasets import make_classification

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class TrainingData:
    features: pd.DataFrame
    target: np.ndarray
    row_ids: np.ndarray
    provenance: dict[str, Any]


def configured(value: object) -> bool:
    return value is not None and str(value).strip() not in {"", "TBD"}


def data_file(cfg: DictConfig, name: str) -> Path:
    base = Path(str(cfg.data.raw_dir)).expanduser()
    if not base.is_absolute():
        base = ROOT / base
    path = Path(name)
    return (path if path.is_absolute() else base / path).resolve()


def fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path, id_column: str | None = None) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Configured data file not found: {path}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        header = next(csv.reader(handle), [])
    if not header or len(header) != len(set(header)) or any(not name for name in header):
        raise ValueError("CSV columns must be nonempty and unique.")
    return pd.read_csv(path, dtype={id_column: str} if id_column else None)


def _check_ids(frame: pd.DataFrame, column: str) -> None:
    if column not in frame:
        raise ValueError(f"ID column missing: {column}")
    if frame[column].isna().any() or not frame[column].is_unique:
        raise ValueError(f"IDs must be non-null and unique: {column}")


def _check_features(frame: pd.DataFrame) -> None:
    if not len(frame) or not len(frame.columns):
        raise ValueError("Features must have rows and columns.")
    numeric = frame.select_dtypes(include="number")
    if np.isinf(numeric.to_numpy(dtype=float)).any():
        raise ValueError("Features contain infinite values.")


def load_train_data(cfg: DictConfig) -> TrainingData:
    mode = cfg.data.mode
    if mode == "synthetic":
        if any(
            configured(cfg.data[key])
            for key in ("train_file", "test_file", "sample_submission_file")
        ):
            raise ValueError("Synthetic mode cannot be combined with configured CSV files.")
        X, y = make_classification(
            n_samples=int(cfg.data.synthetic_samples),
            n_features=20,
            random_state=int(cfg.project.seed),
        )
        frame = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        digest = hashlib.sha256(X.tobytes() + y.tobytes()).hexdigest()
        logger.warning("Explicit synthetic smoke data; scores are not competition performance.")
        return TrainingData(
            frame,
            y,
            np.arange(len(y)),
            {
                "mode": mode,
                "sha256": digest,
                "rows": len(y),
                "generator": "sklearn.make_classification",
            },
        )
    if mode != "csv":
        raise ValueError("data.mode must be synthetic or csv.")
    if not configured(cfg.data.train_file) or not configured(cfg.data.target):
        raise ValueError("CSV mode requires data.train_file and data.target.")
    id_column = str(cfg.data.id_column) if configured(cfg.data.id_column) else None
    path = data_file(cfg, str(cfg.data.train_file))
    frame = read_csv(path, id_column)
    target = str(cfg.data.target)
    if target not in frame or frame[target].isna().any():
        raise ValueError("Target must exist and contain no missing values.")
    if id_column:
        _check_ids(frame, id_column)
        if id_column == target:
            raise ValueError("ID and target columns must differ.")
    y = frame[target].to_numpy()
    if np.issubdtype(y.dtype, np.number) and not np.isfinite(y).all():
        raise ValueError("Target must contain only finite values.")
    if len(pd.unique(y)) < 2:
        raise ValueError("Classification target needs at least two classes.")
    drop = [target] + ([id_column] if id_column else [])
    features = frame.drop(columns=drop)
    _check_features(features)
    row_ids = frame[id_column].to_numpy() if id_column else np.arange(len(frame))
    logger.info("Loaded {} rows from {}", len(frame), path)
    return TrainingData(
        features,
        y,
        row_ids,
        {
            "mode": mode,
            "path": str(path),
            "sha256": fingerprint(path),
            "rows": len(frame),
            "features": features.columns.tolist(),
        },
    )


def load_test_data(cfg: DictConfig, feature_columns: list[str]) -> pd.DataFrame | None:
    if not configured(cfg.data.test_file):
        return None
    id_column = str(cfg.data.id_column) if configured(cfg.data.id_column) else None
    frame = read_csv(data_file(cfg, str(cfg.data.test_file)), id_column)
    missing = set(feature_columns) - set(frame.columns)
    if missing:
        raise ValueError(f"Test data is missing feature columns: {sorted(missing)}")
    _check_features(frame[feature_columns])
    return frame


def save_submission(
    predictions: np.ndarray,
    path: Path,
    cfg: DictConfig,
    test_df: pd.DataFrame,
) -> None:
    if not configured(cfg.data.sample_submission_file) or not configured(cfg.data.id_column):
        raise ValueError("Submission requires sample_submission_file and id_column.")
    id_column = str(cfg.data.id_column)
    sample = read_csv(data_file(cfg, str(cfg.data.sample_submission_file)), id_column)
    column = str(cfg.submission.column) if configured(cfg.submission.column) else cfg.data.target
    if column == id_column or set(sample.columns) != {id_column, column}:
        raise ValueError("Expected exactly the ID and configured prediction columns.")
    _check_ids(sample, id_column)
    _check_ids(test_df, id_column)
    values = np.asarray(predictions)
    if values.ndim != 1 or len(values) != len(test_df) or len(sample) != len(test_df):
        raise ValueError("Prediction length/shape must match test and sample rows.")
    if pd.isna(values).any():
        raise ValueError("Predictions contain missing values.")
    if np.issubdtype(values.dtype, np.number) and not np.isfinite(values).all():
        raise ValueError("Predictions must be finite.")
    if cfg.submission.prediction == "probability":
        if not np.issubdtype(values.dtype, np.number) or ((values < 0) | (values > 1)).any():
            raise ValueError("Probabilities must be numeric and in [0, 1].")
    if set(sample[id_column]) != set(test_df[id_column]):
        raise ValueError("Sample and test IDs do not match.")
    indexed = pd.Series(values, index=test_df[id_column])
    sample[column] = indexed.reindex(sample[id_column]).to_numpy()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", newline="", encoding="utf-8") as handle:
        sample.to_csv(handle, index=False)
    logger.info("Saved ID-aligned submission: {}", path)
