from pathlib import Path
import pandas as pd
from .config import settings
import structlog

log = structlog.get_logger()

def write_gold(silver_parquet_path, out_root=None):
    out_root = Path(out_root or settings.OUTPUT_ROOT) / "gold"
    out_root.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(silver_parquet_path)
    date = df['date'].iloc[0]
    year, month, day = date.split("-")
    target_dir = out_root / f"year={year}" / f"month={month}" / f"day={day}"
    target_dir.mkdir(parents=True, exist_ok=True)
    out_file = target_dir / "rates.parquet"
    df.to_parquet(out_file, index=False, compression="snappy")
    log.info("gold.written", path=str(out_file))
    return out_file
