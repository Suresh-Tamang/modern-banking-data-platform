from __future__ import annotations
from sqlalchemy import create_engine, text
import pandas as pd
import io

def copy_data_to_warehouse(
    dsn: str,
    table: str,
    df: pd.DataFrame
) -> None:
    """
    Upsert transactions into the data warehouse using PostgreSQL COPY command.

    Args:
        dsn (str): The data source name for the PostgreSQL connection.
        table (str): The target table name in the data warehouse.
        df (pd.DataFrame): The DataFrame containing transaction data to be upserted.
    """
    if df.empty:
        return # No data to upsert
    
    
    engine = create_engine(dsn, pool_pre_ping=True)
    with engine.begin() as conn:
        #create a temporary table
        temp_table = f"{table}_staging"
        conn.execute(text(f"""
            CREATE TEMPORARY TABLE {temp_table} (LIKE {table} INCLUDING ALL)
        """))
        
        # use StringIO to simulate a file for COPY
        buffer = io.StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)  
        
        raw = conn.connection
        with raw.cursor() as cur:
            cur.copy_expert(
                f"COPY {temp_table} FROM STDIN WITH CSV",
                buffer
            )
        conn.execute(text(f"INSERT INTO {table} SELECT * FROM {temp_table} ON CONFLICT DO NOTHING"))
    
    