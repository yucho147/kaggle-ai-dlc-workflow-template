"""Run the explicit tabular classification demo: python -m baseline.train."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import hydra
import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from loguru import logger
from omegaconf import DictConfig, OmegaConf

from baseline.data import ROOT, load_test_data, load_train_data, save_submission
from baseline.evaluate import run_cross_validation
from baseline.model import build_model, predict_output
from baseline.tracking import (
    environment_metadata,
    log_config,
    log_cv_results,
    model_requirements,
    resolve_tracking_uri,
    write_manifest,
)


@hydra.main(config_path="../../configs", config_name="baseline", version_base=None)
def main(cfg: DictConfig) -> None:
    started = perf_counter()
    local_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid4().hex[:8]
    output_root = Path(str(cfg.output.dir)).expanduser()
    if not output_root.is_absolute():
        output_root = ROOT / output_root
    run_dir = output_root.resolve() / local_id
    run_dir.mkdir(parents=True, exist_ok=False)
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(run_dir / "run.log", level="DEBUG", encoding="utf-8")
    OmegaConf.save(cfg, run_dir / "config.yaml", resolve=True)
    np.random.seed(int(cfg.project.seed))
    manifest = {
        "local_run_id": local_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "argv": sys.argv[1:],
        "environment": environment_metadata(),
        "config": OmegaConf.to_container(cfg, resolve=True),
        "artifact_dir": str(run_dir),
        "mlflow_uri": resolve_tracking_uri(str(cfg.mlflow.tracking_uri)),
    }
    manifest_path = run_dir / "manifest.json"
    write_manifest(manifest_path, manifest)
    try:
        mlflow.set_tracking_uri(manifest["mlflow_uri"])
        mlflow.set_experiment(str(cfg.mlflow.experiment_name))
        with mlflow.start_run(run_name=str(cfg.mlflow.run_name)) as run:
            manifest["mlflow_run_id"] = run.info.run_id
            log_config(cfg)
            train = load_train_data(cfg)
            manifest["data"] = train.provenance
            mlflow.set_tags(
                {
                    "data_mode": cfg.data.mode,
                    "data_sha256": train.provenance["sha256"],
                    "local_run_id": local_id,
                    "git_commit": manifest["environment"]["git_commit"],
                    "git_dirty": str(manifest["environment"]["git_dirty"]),
                }
            )
            test = load_test_data(cfg, train.features.columns.tolist())
            comparison = run_cross_validation(
                build_model(cfg, dummy=True), train.features, train.target, cfg
            )
            model = build_model(cfg)
            cv = run_cross_validation(model, train.features, train.target, cfg)
            if not np.array_equal(cv.fold_ids, comparison.fold_ids):
                raise ValueError("Baseline and candidate splits do not match.")
            log_cv_results(cv.scores, str(cfg.validation.metric))
            log_cv_results(comparison.scores, str(cfg.validation.metric), prefix="dummy")
            metrics = {
                "scorer": cfg.validation.metric,
                "direction": "maximize",
                "aggregation": "unweighted_fold_mean",
                "fold_scores": cv.scores,
                "cv_mean": float(np.mean(cv.scores)),
                "cv_std": float(np.std(cv.scores)),
                "dummy_fold_scores": comparison.scores,
                "dummy_mean": float(np.mean(comparison.scores)),
                "improvement": float(np.mean(cv.scores) - np.mean(comparison.scores)),
            }
            write_manifest(run_dir / "metrics.json", metrics)
            pd.DataFrame(
                {
                    "row_id": train.row_ids,
                    "target": train.target,
                    "prediction": cv.predictions,
                    "fold_id": cv.fold_ids,
                }
            ).to_csv(run_dir / "oof.csv", index=False)
            manifest.update(split_sha256=cv.split_fingerprint, metrics=metrics)
            model.fit(train.features, train.target)
            joblib.dump(model, run_dir / "model.joblib")
            signature = mlflow.models.infer_signature(train.features, model.predict(train.features))
            model_info = mlflow.sklearn.log_model(
                model, name="model", signature=signature, pip_requirements=model_requirements()
            )
            manifest["mlflow_model_uri"] = model_info.model_uri
            if test is not None:
                values = predict_output(model, test[train.features.columns], cfg)
                save_submission(values, run_dir / "submission.csv", cfg, test)
            manifest.update(status="succeeded", finished_at=datetime.now(timezone.utc).isoformat())
            manifest["duration_seconds"] = perf_counter() - started
            write_manifest(manifest_path, manifest)
            mlflow.log_artifacts(str(run_dir), artifact_path="local_run")
            logger.info("Run {} saved at {}", run.info.run_id, run_dir)
    except Exception as exc:
        manifest.update(
            status="failed",
            error=f"{type(exc).__name__}: {exc}",
            finished_at=datetime.now(timezone.utc).isoformat(),
        )
        logger.exception("Run failed; evidence remains at {}", run_dir)
        raise
    finally:
        if manifest["status"] != "succeeded":
            manifest["duration_seconds"] = perf_counter() - started
        write_manifest(manifest_path, manifest)
        logger.complete()


if __name__ == "__main__":
    main()
