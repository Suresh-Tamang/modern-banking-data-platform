from __future__ import annotations
from sqlalchemy import create_engine, text
import pandas as pd
import io


def copy_dataframe_to_postgres(
    dsn: str,
    table: str,
    df: pd.DataFrame) -> None:
    """Copy a pandas DataFrame to a PostgreSQL table using COPY command for efficiency."""
    if df.empty:
        return
    
    engine = create_engine(dsn, pool_pre_ping=True)
    with engine.begin() as cx:
        cx.execute(text(f"CREATE TEMP TABLE _stg_copy AS TABLE {table} WITH NO DATA"))
        
        # Use StringIO to hold CSV data in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, header=False)
        csv_buffer.seek(0)
        
        raw = cx.connection
        with raw.cursor() as cur:
            cur.copy_expert(
                f"COPY _stg_copy FROM STDIN WITH (FORMAT CSV)", csv_buffer
            )
        cx.execute(text(f"INSERT INTO {table} SELECT * FROM _stg_copy ON CONFLICT DO NOTHING"))