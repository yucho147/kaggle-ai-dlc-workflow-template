"""Fold evidence and out-of-fold predictions for the same explicit scoring protocol."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np
import pandas as pd
from loguru import logger
from omegaconf import DictConfig
from sklearn.base import clone
from sklearn.metrics import get_scorer
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.pipeline import Pipeline

from baseline.model import predict_output


@dataclass
class CVResult:
    scores: list[float]
    predictions: np.ndarray
    fold_ids: np.ndarray

    @property
    def split_fingerprint(self) -> str:
        return hashlib.sha256(self.fold_ids.tobytes()).hexdigest()


def build_cv_splitter(cfg: DictConfig):
    strategy = cfg.validation.strategy
    n_splits = int(cfg.validation.n_splits)
    if n_splits < 2:
        raise ValueError("n_splits must be at least 2.")
    kwargs = {"n_splits": n_splits, "shuffle": True, "random_state": int(cfg.project.seed)}
    if strategy == "stratified_kfold":
        return StratifiedKFold(**kwargs)
    if strategy == "kfold":
        return KFold(**kwargs)
    raise ValueError("Demo supports stratified_kfold / kfold; implement group/time protocols.")


def run_cross_validation(
    model: Pipeline,
    X: pd.DataFrame,
    y: np.ndarray,
    cfg: DictConfig,
) -> CVResult:
    splitter = build_cv_splitter(cfg)
    if len(X) != len(y) or len(y) < splitter.n_splits:
        raise ValueError("Feature/target lengths and split count are inconsistent.")
    if cfg.validation.strategy == "stratified_kfold":
        if pd.Series(y).value_counts().min() < splitter.n_splits:
            raise ValueError("Each class needs at least n_splits observations.")
    scorer = get_scorer(str(cfg.validation.metric))
    predictions = np.empty(
        len(y), dtype=float if cfg.submission.prediction == "probability" else y.dtype
    )
    fold_ids = np.full(len(y), -1, dtype=np.int64)
    scores = []
    for fold, (train, valid) in enumerate(splitter.split(X, y)):
        if np.intersect1d(train, valid).size or np.any(fold_ids[valid] != -1):
            raise ValueError("Split overlaps training/validation or repeats validation rows.")
        fitted = clone(model).fit(X.iloc[train], y[train])
        score = float(scorer(fitted, X.iloc[valid], y[valid]))
        if not np.isfinite(score):
            raise ValueError("Validation produced a non-finite score.")
        scores.append(score)
        predictions[valid] = predict_output(fitted, X.iloc[valid], cfg)
        fold_ids[valid] = fold
    if np.any(fold_ids == -1):
        raise ValueError("OOF predictions do not cover every row.")
    logger.info("CV {}: {:.4f} ± {:.4f}", cfg.validation.metric, np.mean(scores), np.std(scores))
    return CVResult(scores, predictions, fold_ids)
