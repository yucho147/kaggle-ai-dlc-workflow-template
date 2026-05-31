"""Baseline training entrypoint: Hydra + MLflow + loguru.

This is a smoke-test template showing how to wire up the standard stack.
Replace the data loading and model sections for each project.

Run:
    uv run --group research python src/baseline/train.py
    uv run --group research python src/baseline/train.py project.name=my_exp model.params.n_estimators=200
"""

import sys
from datetime import datetime
from pathlib import Path

import hydra
import mlflow
import mlflow.sklearn
import numpy as np
from hydra.utils import to_absolute_path
from loguru import logger
from omegaconf import DictConfig

from baseline.data import load_train_data, save_submission
from baseline.evaluate import run_cross_validation
from baseline.model import build_model
from baseline.tracking import log_config, log_cv_results, resolve_tracking_uri


def setup_logger(log_path: Path) -> None:
    logger.remove()
    logger.add(sys.stderr, level="INFO", colorize=True)
    logger.add(log_path, level="DEBUG", rotation="10 MB", encoding="utf-8")


@hydra.main(config_path="../../configs", config_name="baseline", version_base=None)
def main(cfg: DictConfig) -> None:
    # --- Paths ---
    outputs_dir = Path(to_absolute_path(cfg.output.dir))
    log_dir = outputs_dir / "logs"
    submission_dir = outputs_dir / "submissions"
    log_dir.mkdir(parents=True, exist_ok=True)
    submission_dir.mkdir(parents=True, exist_ok=True)

    # --- Logger ---
    run_name = cfg.mlflow.run_name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    setup_logger(log_dir / f"{run_name}_{timestamp}.log")
    logger.info(f"Starting run: {run_name}")

    # --- Seed ---
    np.random.seed(cfg.project.seed)

    # --- MLflow ---
    mlflow.set_tracking_uri(resolve_tracking_uri(cfg.mlflow.tracking_uri))
    mlflow.set_experiment(cfg.mlflow.experiment_name)

    with mlflow.start_run(run_name=run_name):
        log_config(cfg)

        X, y = load_train_data(cfg)
        model = build_model(cfg)
        scores = run_cross_validation(model, X, y, cfg)
        cv_mean, cv_std = log_cv_results(scores, cfg.validation.metric)
        logger.info(f"CV {cfg.validation.metric}: {cv_mean:.4f} ± {cv_std:.4f}")

        # Train final model on full data
        model.fit(X, y)
        mlflow.sklearn.log_model(model, artifact_path="model")

        # Save and log submission placeholder
        submission_path = submission_dir / f"{run_name}_{timestamp}.csv"
        save_submission(model.predict(X), submission_path)
        mlflow.log_artifact(str(submission_path), artifact_path="submission")

    logger.info("Done.")


if __name__ == "__main__":
    main()
