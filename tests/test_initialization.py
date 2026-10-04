import pytest

from scripts.init_aidlc_docs import initialize


@pytest.fixture
def seed(tmp_path):
    template = tmp_path / "templates"
    (template / "inception").mkdir(parents=True)
    (template / "audit.md").write_text("empty audit")
    (template / "inception/problem.md").write_text("empty problem")
    return template


def test_missing_only_preserves_project_records_and_extra_files(seed, tmp_path):
    target = tmp_path / "project/aidlc-docs"
    target.mkdir(parents=True)
    (target / "audit.md").write_text("important decisions")
    (target / "custom.md").write_text("custom project knowledge")
    code, backup = initialize(seed, target)
    assert code == 0 and backup is None
    assert (target / "audit.md").read_text() == "important decisions"
    assert (target / "custom.md").read_text() == "custom project knowledge"
    assert (target / "inception/problem.md").is_file()
    assert initialize(seed, target, check=True)[0] == 0


def test_check_reports_missing_without_modifying(seed, tmp_path):
    target = tmp_path / "project/aidlc-docs"
    assert initialize(seed, target, check=True)[0] == 1
    assert not target.exists()


@pytest.mark.parametrize("fresh", [False, True])
def test_explicit_reset_backs_up_all_records(seed, tmp_path, fresh):
    target = tmp_path / "project/aidlc-docs"
    target.mkdir(parents=True)
    (target / "audit.md").write_text("important decisions")
    (target / "custom.md").write_text("custom project knowledge")
    code, backup = initialize(seed, target, force=not fresh, new_project=fresh)
    assert code == 0
    assert backup and (backup / "audit.md").read_text() == "important decisions"
    assert (backup / "custom.md").read_text() == "custom project knowledge"
    assert (target / "audit.md").read_text() == "empty audit"
    assert (target / "custom.md").exists() is (not fresh)


def test_repeated_resets_keep_unique_backups(seed, tmp_path):
    target = tmp_path / "project/aidlc-docs"
    initialize(seed, target)
    first = initialize(seed, target, force=True)[1]
    second = initialize(seed, target, force=True)[1]
    assert first != second
    assert first.is_dir() and second.is_dir()


def test_rejects_target_that_contains_seed(seed):
    with pytest.raises(ValueError):
        initialize(seed, seed.parent, new_project=True)


def test_rejects_symlink_target(seed, tmp_path):
    actual = tmp_path / "actual"
    actual.mkdir()
    target = tmp_path / "link"
    target.symlink_to(actual, target_is_directory=True)
    with pytest.raises(ValueError):
        initialize(seed, target, force=True)
    assert not list(actual.iterdir())


def test_rejects_nested_symlink_escape(seed, tmp_path):
    target = tmp_path / "project/aidlc-docs"
    target.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (target / "inception").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        initialize(seed, target)
    assert not (outside / "problem.md").exists()
