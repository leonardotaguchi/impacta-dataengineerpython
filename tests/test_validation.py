import pandas as pd
from src.fx_pipeline.transform import validate
import pytest

def test_validate_positive_rates():
    df = pd.DataFrame({
        "date":["2025-01-01"],
        "timestamp":[0],
        "base_currency":["USD"],
        "target_currency":["BRL"],
        "rate":[5.2]
    })
    assert validate(df) is True

def test_validate_negative_rates_raises():
    df = pd.DataFrame({
        "date":["2025-01-01"],
        "timestamp":[0],
        "base_currency":["USD"],
        "target_currency":["BRL"],
        "rate":[-1.0]
    })
    with pytest.raises(ValueError):
        validate(df)
