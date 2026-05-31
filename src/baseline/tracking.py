"""MLflow tracking utilities."""

import mlflow
from hydra.utils import to_absolute_path
from omegaconf import DictConfig, OmegaConf


def resolve_tracking_uri(uri: str) -> str:
    """Resolve tracking URI to absolute path only for filesystem paths.

    URIs with a scheme (sqlite://, http://, etc.) are returned as-is because
    to_absolute_path() would corrupt the scheme prefix.
    """
    if "://" in uri:
        return uri
    return to_absolute_path(uri)


def flatten_config(cfg: dict, parent_key: str = "", sep: str = ".") -> dict[str, object]:
    """Flatten nested config dict to scalar key-value pairs for mlflow.log_params."""
    items: list[tuple[str, object]] = []
    for k, v in cfg.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_config(v, new_key, sep).items())
        elif isinstance(v, list):
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)


def log_config(cfg: DictConfig) -> None:
    """Log scalar params to MLflow and save full config as artifact."""
    cfg_dict = OmegaConf.to_container(cfg, resolve=True)
    flat = flatten_config(cfg_dict)
    mlflow.log_params({k: v for k, v in flat.items() if not isinstance(v, (dict, list))})
    mlflow.log_dict(cfg_dict, "config_resolved.json")


def log_cv_results(scores: list[float], metric_name: str) -> tuple[float, float]:
    """Log CV mean/std to MLflow and return them."""
    import numpy as np

    cv_mean = float(np.mean(scores))
    cv_std = float(np.std(scores))
    mlflow.log_metric("cv_score", cv_mean)
    mlflow.log_metric("cv_std", cv_std)
    return cv_mean, cv_std
