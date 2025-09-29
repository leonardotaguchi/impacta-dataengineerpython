# FX Pipeline Template

Pipeline to ingest exchange rates from ExchangeRate-API, normalize, validate and enrich with an LLM (OpenAI).
Structure: raw -> silver -> gold. Includes logging, tests and CI example.

## Quickstart

1. Copy `.env.example` to `.env` and fill keys:
   - EXR_API_KEY
   - OPENAI_API_KEY

2. Create venv and install:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run:
```bash
python run_daily.py
```

Outputs are produced under `data/`:
- `data/raw/YYYY-MM-DD.json`
- `data/silver/YYYY-MM-DD/`
- `data/gold/year=.../month=.../day=.../rates.parquet`
- `data/gold/insights/YYYY-MM-DD.txt`

See `src/fx_pipeline` for implementation details.
