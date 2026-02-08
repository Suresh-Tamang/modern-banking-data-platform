from __future__ import annotations
import os, yaml 
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"/"settings.yaml"

def load_settings() -> dict:
    """Load configuration settings from a YAML file."""
    with open(CONFIG_DIR, 'r') as f:
        settings = yaml.safe_load(f)
    return settings


def env(key: str) -> str:
    """Get environment variable or raise error if not found."""
    value = os.getenv(key)
    if value is None:
        raise EnvironmentError(f"Environment variable '{key}' not found.")
    return value