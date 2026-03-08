from __future__ import annotations
import os, yaml
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR/"config"/"settings.yaml"

def load_settings()-> dict:
    """Load settings from the YAML configuration file."""   
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def env(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise EnvironmentError(f"Environment variable '{key}' not f ound.")
    return val
 
