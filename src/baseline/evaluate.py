"""Cross-validation logic."""

import numpy as np
from loguru import logger
from omegaconf import DictConfig
from sklearn.base import BaseEstimator
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score


def build_cv_splitter(cfg: DictConfig):
    """Build a CV splitter from validation config."""
    strategy = cfg.validation.strategy
    n_splits = cfg.validation.n_splits
    seed = cfg.project.seed

    if strategy == "stratified_kfold":
        return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    if strategy == "kfold":
        return KFold(n_splits=n_splits, shuffle=True, random_state=seed)

    raise ValueError(f"Unknown validation strategy: {strategy}. Add it to src/baseline/evaluate.py.")


def run_cross_validation(
    model: BaseEstimator,
    X: np.ndarray,
    y: np.ndarray,
    cfg: DictConfig,
) -> list[float]:
    """Run cross-validation and return per-fold scores."""
    cv = build_cv_splitter(cfg)
    scores = cross_val_score(model, X, y, cv=cv, scoring=cfg.validation.metric)
    logger.info(f"CV {cfg.validation.metric}: {scores.mean():.4f} ± {scores.std():.4f}")
    return scores.tolist()
