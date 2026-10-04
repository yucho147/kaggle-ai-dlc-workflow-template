"""Tracking paths and a local manifest survive beyond one interactive session."""

from __future__ import annotations

import json
import platform
import subprocess
from importlib.metadata import distributions, version
from pathlib import Path
from typing import Any

import mlflow
import numpy as np
from omegaconf import DictConfig, OmegaConf

ROOT = Path(__file__).resolve().parents[2]


def resolve_tracking_uri(uri: str) -> str:
    if uri.startswith("sqlite:///"):
        database, separator, query = uri[len("sqlite:///") :].partition("?")
        path = Path(database).expanduser()
        if not path.is_absolute():
            path = ROOT / path
        return "sqlite:///" + str(path.resolve()) + (separator + query if separator else "")
    if "://" in uri:
        return uri
    return str((ROOT / Path(uri).expanduser()).resolve())


def flatten_config(cfg: dict, parent_key: str = "") -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in cfg.items():
        name = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            result.update(flatten_config(value, name))
        else:
            result[name] = (
                json.dumps(value, ensure_ascii=False) if isinstance(value, list) else value
            )
    return result


def log_config(cfg: DictConfig) -> None:
    values = OmegaConf.to_container(cfg, resolve=True)
    mlflow.log_params(flatten_config(values))
    mlflow.log_dict(values, "config_resolved.json")


def model_requirements() -> list[str]:
    # MLflow's automatic uv export can omit dependencies from research groups.
    packages = ("mlflow", "scikit-learn", "numpy", "scipy", "pandas", "joblib", "cloudpickle")
    return [f"{name}=={version(name)}" for name in packages]


def log_cv_results(scores: list[float], metric_name: str, prefix: str = "cv") -> None:
    mlflow.set_tag("scorer", metric_name)
    mlflow.set_tag("score_direction", "maximize")
    mlflow.log_metric(f"{prefix}_score", float(np.mean(scores)))
    mlflow.log_metric(f"{prefix}_std", float(np.std(scores)))
    for index, score in enumerate(scores):
        mlflow.log_metric(f"{prefix}_fold_{index}", score)


def environment_metadata() -> dict[str, Any]:
    def git(args: list[str]) -> str:
        try:
            result = subprocess.run(
                ["git", *args], cwd=ROOT, text=True, capture_output=True, timeout=5, check=False
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except (OSError, subprocess.TimeoutExpired):
            return "unknown"

    status = git(["status", "--porcelain"])
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "git_commit": git(["rev-parse", "HEAD"]),
        "git_dirty": status != "" if status != "unknown" else None,
        "packages": {
            dist.metadata["Name"]: dist.version for dist in distributions() if dist.metadata["Name"]
        },
    }


def write_manifest(path: Path, values: dict[str, Any]) -> None:
    path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")
