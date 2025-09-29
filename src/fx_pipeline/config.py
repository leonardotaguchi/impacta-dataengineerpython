from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class Settings:
    EXR_API_KEY = os.getenv("EXR_API_KEY")
    EXR_BASE = os.getenv("EXR_BASE", "USD")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OUTPUT_ROOT = Path(os.getenv("OUTPUT_ROOT", "./data"))
    DB_URL = os.getenv("DB_URL")
    ENV = os.getenv("ENV", "dev")

settings = Settings()
