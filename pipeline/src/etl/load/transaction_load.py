from __future__ import annotations
from sqlalchemy import create_engine, text
import pandas as pd
import io


def copy_data_to_warehouse(
    dsn: str,
    table: str,
    df: pd.DataFrame
) -> None:

    if df.empty:
        return

    engine = create_engine(dsn, pool_pre_ping=True)

    with engine.begin() as conn:
        temp_table = f"{table}_staging"

        conn.execute(text(f"""
            CREATE TEMPORARY TABLE {temp_table} (LIKE {table} INCLUDING ALL)
        """))

        buffer = io.StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        raw = conn.connection
        with raw.cursor() as cur:
            cur.copy_expert(
                f"COPY {temp_table} FROM STDIN WITH CSV",
                buffer
            )
        raw.commit()

        conn.execute(text(f"""
            INSERT INTO {table}
            SELECT * FROM {temp_table}
            ON CONFLICT DO NOTHING
        """))
