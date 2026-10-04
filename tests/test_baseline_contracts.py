import numpy as np
import pandas as pd
import pytest
from sklearn.impute import SimpleImputer

from baseline.data import load_test_data, load_train_data, read_csv, save_submission
from baseline.evaluate import build_cv_splitter, run_cross_validation
from baseline.model import build_model, predict_output
from baseline.tracking import resolve_tracking_uri


def csv_config(cfg, tmp_path):
    cfg.data.mode = "csv"
    cfg.data.raw_dir = str(tmp_path)
    cfg.data.train_file = "train.csv"
    cfg.data.target = "target"
    cfg.data.id_column = "id"
    return cfg


def test_missing_configured_train_never_falls_back(cfg, tmp_path):
    csv_config(cfg, tmp_path)
    with pytest.raises(FileNotFoundError):
        load_train_data(cfg)


def test_synthetic_is_explicit_and_rejects_csv_mix(cfg):
    cfg.data.train_file = "missing.csv"
    with pytest.raises(ValueError):
        load_train_data(cfg)


def test_csv_preserves_leading_zero_ids_and_missing_features(cfg, tmp_path):
    csv_config(cfg, tmp_path)
    pd.DataFrame(
        {
            "id": ["001", "002", "003", "004"],
            "target": [0, 1, 0, 1],
            "numeric": [1, np.nan, 3, 4],
            "category": ["a", "b", "a", "b"],
        }
    ).to_csv(tmp_path / "train.csv", index=False)
    data = load_train_data(cfg)
    assert data.row_ids.tolist() == ["001", "002", "003", "004"]
    assert data.features.columns.tolist() == ["numeric", "category"]
    assert len(data.provenance["sha256"]) == 64
    assert data.features["numeric"].isna().sum() == 1


def test_configured_missing_test_is_error(cfg, tmp_path):
    csv_config(cfg, tmp_path)
    cfg.data.test_file = "missing.csv"
    with pytest.raises(FileNotFoundError):
        load_test_data(cfg, ["numeric"])


def test_duplicate_column_names_are_rejected(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("id,x,x\n1,2,3\n")
    with pytest.raises(ValueError):
        read_csv(path)


def test_nonfinite_target_is_rejected(cfg, tmp_path):
    csv_config(cfg, tmp_path)
    pd.DataFrame({"id": ["a", "b"], "target": [0, np.inf], "x": [1, 2]}).to_csv(
        tmp_path / "train.csv", index=False
    )
    with pytest.raises(ValueError):
        load_train_data(cfg)


def test_imputation_is_fit_only_on_training_fold(cfg, monkeypatch):
    frame = pd.DataFrame(
        {
            "numeric": [0, 2, np.nan, 6, 8, 10, 100, 102, np.nan, 106, 108, 110],
            "category": ["a", "b"] * 6,
        }
    )
    target = np.array([0, 1] * 6)
    fitted_rows = []
    original = SimpleImputer.fit

    def record_fit(self, X, y=None):
        fitted_rows.append(frozenset(X.index))
        return original(self, X, y)

    monkeypatch.setattr(SimpleImputer, "fit", record_fit)
    result = run_cross_validation(build_model(cfg), frame, target, cfg)
    expected = {frozenset(train) for train, _ in build_cv_splitter(cfg).split(frame, target)}
    assert set(fitted_rows) == expected
    assert all(len(rows) == 8 for rows in fitted_rows)
    assert np.all(result.fold_ids >= 0)
    assert len(result.predictions) == len(frame)
    assert len(result.split_fingerprint) == 64


def test_oof_is_repeatable_and_unknown_categories_are_supported(cfg):
    frame = pd.DataFrame({"x": range(12), "category": ["a", "b"] * 6})
    target = np.array([0, 1] * 6)
    first = run_cross_validation(build_model(cfg), frame, target, cfg)
    second = run_cross_validation(build_model(cfg), frame, target, cfg)
    np.testing.assert_array_equal(first.predictions, second.predictions)
    assert first.split_fingerprint == second.split_fingerprint
    model = build_model(cfg).fit(frame, target)
    assert len(model.predict(pd.DataFrame({"x": [5], "category": ["new"]}))) == 1


def test_probability_uses_the_requested_positive_class(cfg):
    frame = pd.DataFrame({"x": range(12)})
    target = np.array(["yes", "no"] * 6)
    model = build_model(cfg).fit(frame, target)
    cfg.submission.prediction = "probability"
    cfg.submission.positive_label = "yes"
    expected = model.predict_proba(frame)[:, model.classes_.tolist().index("yes")]
    np.testing.assert_allclose(predict_output(model, frame, cfg), expected)
    cfg.submission.positive_label = "unknown"
    with pytest.raises(ValueError):
        predict_output(model, frame, cfg)


def test_boolean_features_work_without_numeric_or_string_columns(cfg):
    frame = pd.DataFrame({"flag": [True, False] * 6})
    model = build_model(cfg).fit(frame, np.array([0, 1] * 6))
    assert model.predict(frame).shape == (12,)


def test_submission_aligns_ids_and_retains_column_order(cfg, tmp_path):
    cfg.data.raw_dir = str(tmp_path)
    cfg.data.sample_submission_file = "sample.csv"
    cfg.data.id_column = "id"
    cfg.submission.column = "prediction"
    cfg.submission.prediction = "probability"
    pd.DataFrame({"prediction": [0.0, 0.0], "id": ["001", "002"]}).to_csv(
        tmp_path / "sample.csv", index=False
    )
    test = pd.DataFrame({"id": ["002", "001"]})
    output = tmp_path / "submission.csv"
    save_submission(np.array([0.8, 0.2]), output, cfg, test)
    result = read_csv(output, "id")
    assert result.columns.tolist() == ["prediction", "id"]
    assert result["id"].tolist() == ["001", "002"]
    np.testing.assert_allclose(result["prediction"], [0.2, 0.8])


@pytest.mark.parametrize("issue", ["duplicate", "mismatch", "nan", "infinite", "range", "length"])
def test_submission_rejects_contract_violations(cfg, tmp_path, issue):
    cfg.data.raw_dir = str(tmp_path)
    cfg.data.sample_submission_file = "sample.csv"
    cfg.data.id_column = "id"
    cfg.submission.column = "prediction"
    cfg.submission.prediction = "probability"
    pd.DataFrame({"id": ["a", "b"], "prediction": [0.0, 0.0]}).to_csv(
        tmp_path / "sample.csv", index=False
    )
    test = pd.DataFrame({"id": ["a", "b"]})
    values = np.array([0.2, 0.8])
    if issue == "duplicate":
        test["id"] = ["a", "a"]
    elif issue == "mismatch":
        test["id"] = ["a", "c"]
    elif issue == "nan":
        values[0] = np.nan
    elif issue == "infinite":
        values[0] = np.inf
    elif issue == "range":
        values[0] = 1.1
    elif issue == "length":
        values = values[:1]
    with pytest.raises(ValueError):
        save_submission(values, tmp_path / "output.csv", cfg, test)
    assert not (tmp_path / "output.csv").exists()


def test_submission_requires_a_real_template(cfg, tmp_path):
    with pytest.raises(ValueError):
        save_submission(np.array([0]), tmp_path / "out.csv", cfg, pd.DataFrame({"id": ["a"]}))


def test_sqlite_tracking_path_does_not_depend_on_working_directory(monkeypatch, tmp_path):
    from baseline import tracking

    monkeypatch.setattr(tracking, "ROOT", tmp_path)
    assert resolve_tracking_uri("sqlite:///mlruns.db") == f"sqlite:///{tmp_path}/mlruns.db"
    assert resolve_tracking_uri("https://tracking.example") == "https://tracking.example"
    assert (
        resolve_tracking_uri(f"sqlite:///{tmp_path}/db.sqlite") == f"sqlite:///{tmp_path}/db.sqlite"
    )
