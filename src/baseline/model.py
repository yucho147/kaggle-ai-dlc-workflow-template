"""Classification pipelines fit imputation and category encoding inside each fold."""

from __future__ import annotations

import numpy as np
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder


def build_model(cfg: DictConfig, *, dummy: bool = False) -> Pipeline:
    if dummy:
        estimator = DummyClassifier(strategy="most_frequent")
    elif cfg.model.name == "random_forest":
        params = dict(OmegaConf.to_container(cfg.model.params, resolve=True))
        params.setdefault("random_state", int(cfg.project.seed))
        estimator = RandomForestClassifier(**params)
    else:
        raise ValueError(f"Unsupported model: {cfg.model.name}")
    categorical = Pipeline(
        [
            ("as_object", FunctionTransformer(pd.DataFrame.astype, kw_args={"dtype": object})),
            ("impute", SimpleImputer(strategy="most_frequent", keep_empty_features=True)),
            ("encode", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    numeric = SimpleImputer(strategy="median", keep_empty_features=True)
    preprocessing = ColumnTransformer(
        [
            ("numeric", numeric, make_column_selector(dtype_include=np.number)),
            ("categorical", categorical, make_column_selector(dtype_exclude=np.number)),
        ]
    )
    return Pipeline([("preprocess", preprocessing), ("model", estimator)])


def predict_output(model: Pipeline, frame: pd.DataFrame, cfg: DictConfig) -> np.ndarray:
    if cfg.submission.prediction == "label":
        return model.predict(frame)
    if cfg.submission.prediction != "probability":
        raise ValueError("submission.prediction must be label or probability.")
    classes = model.classes_.tolist()
    positive = cfg.submission.positive_label
    if len(classes) != 2 or positive not in classes:
        raise ValueError("Binary probability requires the configured positive_label.")
    return model.predict_proba(frame)[:, classes.index(positive)]
