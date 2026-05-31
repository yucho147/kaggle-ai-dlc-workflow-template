"""Data loading and submission saving.

Replace `load_train_data` with actual data loading logic for each project.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from omegaconf import DictConfig
from sklearn.datasets import make_classification


def load_train_data(cfg: DictConfig) -> tuple[np.ndarray, np.ndarray]:
    """Load training data. Falls back to dummy data if train_file is not configured.

    Replace this function with actual data loading per project.
    """
    train_file = Path(cfg.data.raw_dir) / cfg.data.train_file
    if cfg.data.train_file == "TBD" or not train_file.exists():
        logger.warning("train_file not configured or not found — using dummy data for smoke test")
        X, y = make_classification(n_samples=1000, n_features=20, random_state=cfg.project.seed)
        return X, y

    df = pd.read_csv(train_file)
    y = df[cfg.data.target].to_numpy()
    X = df.drop(columns=[cfg.data.target, cfg.data.id_column]).to_numpy()
    logger.info(f"Loaded {len(df)} rows from {train_file}")
    return X, y


def save_submission(predictions: np.ndarray, path: Path) -> None:
    """Save prediction array as a submission CSV placeholder."""
    pd.DataFrame({"id": range(len(predictions)), "target": predictions}).to_csv(path, index=False)
    logger.info(f"Submission saved: {path}")
