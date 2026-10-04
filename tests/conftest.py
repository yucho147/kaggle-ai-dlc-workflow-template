from pathlib import Path
import sys

import pytest
from omegaconf import OmegaConf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture
def cfg():
    config = OmegaConf.load(ROOT / "configs/baseline.yaml")
    config.model.params.n_estimators = 3
    config.validation.n_splits = 3
    config.data.synthetic_samples = 60
    return config
