from __future__ import annotations
import pandas as pd
from pathlib import Path
import logging

ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent

def read_file(path: str, fmt: str="csv") -> pd.DataFrame:
    file_path = ROOT_PATH / path
    path_obj = Path(file_path)
    if not path_obj.exists():
        raise FileNotFoundError(f"File not found: {path}")
    logging.info(f"File not found: {path}")
    if fmt == "csv":
        return pd.read_csv(path)
    elif fmt == "json":
        return pd.read_json(path)
    elif fmt == "xlsx":
        return pd.read_excel(path)
    elif fmt == "parquet":
        return pd.read_parquet(path)
    else:
        raise ValueError(f"Unsupported file format: {fmt}")
    