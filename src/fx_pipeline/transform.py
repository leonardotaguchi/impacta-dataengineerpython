import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import structlog
from .config import settings

log = structlog.get_logger()

def load_raw(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(raw_json):
    base = raw_json.get("base_code") or raw_json.get("base")
    ts = raw_json.get("time_last_update_unix") or int(datetime.utcnow().timestamp())
    date = raw_json.get("time_last_update_utc") or datetime.utcnow().isoformat()
    rates = raw_json.get("conversion_rates") or raw_json.get("rates") or {}
    rows = []
    for target, rate in rates.items():
        rows.append({
            "date": date[:10],
            "timestamp": int(ts),
            "base_currency": base,
            "target_currency": target,
            "rate": float(rate),
        })
    df = pd.DataFrame(rows)
    return df

def validate(df):
    if (df['rate'] <= 0).any():
        bad = df[df['rate'] <= 0]
        log.error("validation.failed.non_positive_rates", count=len(bad))
        raise ValueError("Found non-positive exchange rates")
    return True

def save_silver(df, out_root=None):
    out_root = Path(out_root or settings.OUTPUT_ROOT) / "silver"
    out_root.mkdir(parents=True, exist_ok=True)
    dt = df['date'].iloc[0]
    path = out_root / dt
    path.mkdir(exist_ok=True, parents=True)
    csv_path = path / "rates.csv"
    parquet_path = path / "rates.parquet"
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)
    log.info("silver.saved", csv=str(csv_path), parquet=str(parquet_path))
    return parquet_path
