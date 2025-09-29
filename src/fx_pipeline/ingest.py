import requests, json
from datetime import date, datetime
from pathlib import Path
from .config import settings
import structlog

log = structlog.get_logger()

def fetch_latest_rates(base=None):
    base = base or settings.EXR_BASE
    key = settings.EXR_API_KEY
    url = f"https://v6.exchangerate-api.com/v6/{key}/latest/{base}"
    log.info("fetch.start", url=url, base=base)
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    log.info("fetch.success", base=base, timestamp=datetime.utcnow().isoformat())
    return data

def save_raw(data, out_root=None):
    out_root = out_root or settings.OUTPUT_ROOT
    raw_dir = Path(out_root) / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    dt = date.today().isoformat()
    filepath = raw_dir / f"{dt}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.info("raw.saved", path=str(filepath))
    return filepath
