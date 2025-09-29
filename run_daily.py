from src.fx_pipeline.ingest import fetch_latest_rates, save_raw
from src.fx_pipeline.transform import load_raw, normalize, validate, save_silver
from src.fx_pipeline.load import write_gold
from src.fx_pipeline.llm import generate_insight
from src.fx_pipeline.utils import compute_summary
from pathlib import Path

def run():
    raw = fetch_latest_rates()
    raw_path = save_raw(raw)
    raw_json = load_raw(raw_path)
    df = normalize(raw_json)
    validate(df)
    silver_path = save_silver(df)
    gold_path = write_gold(silver_path)
    summary = compute_summary(df)
    insight = generate_insight(summary, df['date'].iloc[0], df['base_currency'].iloc[0])
    out = Path("data/gold/insights")
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{df['date'].iloc[0]}.txt").write_text(insight, encoding="utf-8")

if __name__ == "__main__":
    run()
