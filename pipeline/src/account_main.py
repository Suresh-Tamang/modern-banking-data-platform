from __future__ import annotations
import logging
import pandas as pd

from src import config
from src.logging_setup import setup_logging
from src.etl.extract import transaction_extraction
from src.etl.transform import transaction_transformation
from pipeline.src.etl.load import transaction_load


def run() -> None:
    """Main function to run the ETL process for transactions."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # extract data
    rows = []

    transaction_api = transaction_extraction.TransactionClient(
        api_url=config.env("TRANSACTION_API_URL"),
        api_key=config.env("TRANSACTION_API_KEY")
    )
    logger.info("Starting data extraction from Transaction API.")
    for record in transaction_api.fetch_all_transactions():
        rows.append(record)
    logger.info(f"Extracted {len(rows)} records from Transaction API.")
    if not rows:
        logger.info("No data extracted. Exiting ETL process.")
        return
    # transform data
    logger.info("Starting data transformation.")
    df_raw = pd.DataFrame(rows)
    df_transformed = transaction_transformation.transform_transactions(df_raw)
    logger.info(f"Transformed data into {len(df_transformed)} records.")
    if df_transformed.empty:
        logger.info(
            "No data to load after transformation. Exiting ETL process.")
        return
    # load data
    logger.info("Starting data load into the data warehouse.")
    transaction_load.copy_data_to_warehouse(
        dsn=config.env("DATA_WAREHOUSE_DSN"),
        table=config.env("TRANSACTION_TABLE"),
        df=df_transformed
    )
    logger.info("Data load completed successfully.")


if __name__ == "__main__":
    run()
