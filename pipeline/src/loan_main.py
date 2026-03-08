from __future__ import annotations
import argparse
import logging
import pandas as pd

from src import config
from src.logging_setup import setup_logging
from src.etl.extract import api_client, file_reader, db_reader
from src.etl.transform.core import normalize_loans
from src.etl.load.postgres_copy import copy_dataframe_to_postgres
from src.etl.load.postgres_upsert import upsert_into_postgres


def run(source: str, load_mode: str) -> None:
    cfg = config.load_settings()
    setup_logging()
    log = logging.getLogger(__name__)

    # extract data
    rows = []
    if source == "api":
        api = api_client.ApiClient(
            base_url=config.env("API_BASE_URL"),
            api_key=config.env("API_KEY")
        )
        try:
            rows = list(api.paginate(
                endpoint=cfg["sources"]["api"]["endpoint_loans"]))
            log.info(f"Retrieved {len(rows)} records from API")
        except Exception as e:
            log.error(f"Error retrieving data from API: {str(e)}")
            raise
    elif source == "file":
        df = file_reader.read_file(cfg["sources"]["file"]["path"])
        rows = df.to_dict('records')
        log.info(f"Retrieved {len(rows)} records from File")
    elif source == "db":
        engine = db_reader.connect(config.env("POSTGRES_DSN"))
        rows = []
        for chunk in db_reader.read_in_chunks(
            engine=engine,
            sql=cfg["sources"]["db"]["query"],
            params={},
        ):
            rows.extend(chunk)
        log.info(f"Retrieved {len(rows)} records from db")
    else:
        raise SystemExit(f"Unsupported source: {source}")

    log.info(f"Extracted {len(rows)} rows from {source}")

    normalized = [c.model_dump() for c in normalize_loans(rows)]

    # load
    dsn = config.env("POSTGRES_DSN")
    target_table = cfg["run"]["loans_table"]

    if load_mode == "copy":
        df = pd.DataFrame(normalized)
        copy_dataframe_to_postgres(dsn, target_table, df)
        log.info(
            f"Loaded {len(normalized)} rows into {target_table} using copy")
    elif load_mode == "upsert":
        df = pd.DataFrame(normalized)
        # converting dataframt to list of dicts
        data = df.to_dict(orient='records')
        upsert_into_postgres(dsn, target_table, data,
                             cfg["sources"]["load"]["key_columns"])
        log.info(
            f"Loaded {len(normalized)} rows into {target_table} using upsert")
    else:
        raise SystemExit(f"Unsupported load mode: {load_mode}")
    log.info(
        f"ETL process completed successfully. Loaded {len(normalized)} rows into {target_table}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Pipeline")
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Data source: api, file, db",
    )
    parser.add_argument(
        "--load-mode",
        type=str,
        required=True,
        help="Load mode: copy, upsert",
    )
    args = parser.parse_args()
    run(args.source, args.load_mode)
