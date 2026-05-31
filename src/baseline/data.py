"""Data loading and submission saving.

Replace these functions with project-specific schema and feature logic when
moving beyond the smoke-test baseline.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from hydra.utils import to_absolute_path
from loguru import logger
from omegaconf import DictConfig
from sklearn.datasets import make_classification


def _is_configured(value: object) -> bool:
    return value is not None and str(value).strip() not in {"", "TBD"}


def _data_file(raw_dir: str, file_name: str) -> Path:
    return Path(to_absolute_path(str(Path(raw_dir) / file_name)))


def _dummy_train_data(seed: int) -> tuple[np.ndarray, np.ndarray, list[str]]:
    X, y = make_classification(n_samples=1000, n_features=20, random_state=seed)
    feature_columns = [f"feature_{idx}" for idx in range(X.shape[1])]
    return X, y, feature_columns


def _feature_columns(df: pd.DataFrame, cfg: DictConfig) -> list[str]:
    if not _is_configured(cfg.data.target):
        raise ValueError("data.target must be configured when train_file is used.")

    target = str(cfg.data.target)
    if target not in df.columns:
        raise ValueError(f"Target column not found in train data: {target}")

    drop_columns = {target}
    if _is_configured(cfg.data.id_column):
        drop_columns.add(str(cfg.data.id_column))

    return [column for column in df.columns if column not in drop_columns]


def load_train_data(cfg: DictConfig) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Load training data. Falls back to dummy data if train_file is not configured.

    Replace this function with actual data loading per project.
    """
    if not _is_configured(cfg.data.train_file):
        logger.warning("train_file not configured or not found - using dummy data for smoke test")
        return _dummy_train_data(cfg.project.seed)

    train_file = _data_file(cfg.data.raw_dir, str(cfg.data.train_file))
    if not train_file.exists():
        logger.warning("train_file not configured or not found - using dummy data for smoke test")
        return _dummy_train_data(cfg.project.seed)

    df = pd.read_csv(train_file)
    feature_columns = _feature_columns(df, cfg)
    y = df[str(cfg.data.target)].to_numpy()
    X = df[feature_columns].to_numpy()
    logger.info(f"Loaded {len(df)} rows from {train_file}")
    return X, y, feature_columns


def load_test_data(
    cfg: DictConfig,
    feature_columns: list[str],
) -> tuple[np.ndarray, pd.DataFrame] | None:
    """Load test data for submission generation.

    Returns None when no test file is configured so smoke-test runs do not create
    a misleading train-prediction submission file.
    """
    if not _is_configured(cfg.data.test_file):
        logger.info("test_file not configured; skipping submission generation")
        return None

    test_file = _data_file(cfg.data.raw_dir, str(cfg.data.test_file))
    if not test_file.exists():
        logger.info(f"test_file not found; skipping submission generation: {test_file}")
        return None

    df = pd.read_csv(test_file)
    missing_columns = [column for column in feature_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Test data is missing feature columns: {missing_columns}")

    X = df[feature_columns].to_numpy()
    logger.info(f"Loaded {len(df)} test rows from {test_file}")
    return X, df


def _prediction_column(sample_submission: pd.DataFrame, cfg: DictConfig) -> str:
    id_column = str(cfg.data.id_column) if _is_configured(cfg.data.id_column) else None
    target = str(cfg.data.target) if _is_configured(cfg.data.target) else None

    if target and target in sample_submission.columns and target != id_column:
        return target

    candidate_columns = [column for column in sample_submission.columns if column != id_column]
    if len(candidate_columns) == 1:
        return candidate_columns[0]

    raise ValueError(
        "Could not infer a single prediction column from sample_submission_file. "
        "Configure data.target or customize save_submission."
    )


def save_submission(
    predictions: np.ndarray,
    path: Path,
    cfg: DictConfig,
    test_df: pd.DataFrame,
) -> None:
    """Save predictions using sample_submission when available."""
    sample_path = (
        _data_file(cfg.data.raw_dir, str(cfg.data.sample_submission_file))
        if _is_configured(cfg.data.sample_submission_file)
        else None
    )

    if sample_path and sample_path.exists():
        submission = pd.read_csv(sample_path)
        if len(submission) != len(predictions):
            raise ValueError(
                "Prediction length does not match sample_submission rows: "
                f"{len(predictions)} != {len(submission)}"
            )
        submission[_prediction_column(submission, cfg)] = predictions
    else:
        id_column = str(cfg.data.id_column) if _is_configured(cfg.data.id_column) else "id"
        target = str(cfg.data.target) if _is_configured(cfg.data.target) else "target"
        ids = test_df[id_column] if id_column in test_df.columns else range(len(predictions))
        submission = pd.DataFrame({id_column: ids, target: predictions})
        logger.warning(
            "sample_submission_file not configured or not found; "
            "created fallback submission format"
        )

    submission.to_csv(path, index=False)
    logger.info(f"Submission saved: {path}")
