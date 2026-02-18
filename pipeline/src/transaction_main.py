from __future__ import annotations
import logging
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


from . import config
from .logging_setup import setup_logging
from .etl.extract.transactions_extraction import TransactionClient
from .etl.transform.transaction_transformation import transform_transactions
from .etl.load.transaction_load import copy_data_to_warehouse


def run() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    

    rows = []

    transaction_api = TransactionClient(
        base_url=config.env("TRANSACTION_API_URL"),
        api_key=config.env("API_KEY")
    )

    logger.info("Starting data extraction from Transaction API.")

    for record in transaction_api.paginate("transactions"):
        rows.append(record)

    logger.info(f"Extracted {len(rows)} records from Transaction API.")

    if not rows:
        logger.info("No data extracted. Exiting ETL process.")
        return

    logger.info("Starting data transformation.")
    df_transformed = transform_transactions(rows)

    logger.info(f"Transformed data into {len(df_transformed)} records.")

    if df_transformed.empty:
        logger.info(
            "No data to load after transformation. Exiting ETL process.")
        return

    logger.info("Starting data load into the data warehouse.")

    copy_data_to_warehouse(
        dsn=config.env("DATA_WAREHOUSE_DSN"),
        table=config.env("TRANSACTION_TABLE"),
        df=df_transformed
    )

    logger.info("Data load completed successfully.")


if __name__ == "__main__":
    run()
