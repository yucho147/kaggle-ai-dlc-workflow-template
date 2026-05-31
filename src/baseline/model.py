"""Model factory.

Add model types here as the project grows.
"""

from loguru import logger
from omegaconf import DictConfig
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier


def build_model(cfg: DictConfig) -> BaseEstimator:
    """Build a model from config. Replace or extend for each project."""
    model_name = cfg.model.name
    params = dict(cfg.model.params)
    params.setdefault("random_state", cfg.project.seed)

    if model_name == "random_forest":
        model = RandomForestClassifier(**params)
    else:
        raise ValueError(f"Unknown model: {model_name}. Add it to src/baseline/model.py.")

    logger.info(f"Built model: {model_name} params={params}")
    return model
