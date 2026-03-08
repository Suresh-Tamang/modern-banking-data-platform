from sqlalchemy import create_engine, text


def _chunks(seq, size):
    buf = []
    for item in seq:
        buf.append(item)
        if len(buf) >= size:
            yield buf
            buf = []
    if buf:
        yield buf

def upsert_into_postgres(dsn, table, rows, key_cols):
    """Upsert rows into a PostgreSQL table based on key columns."""
    eng = create_engine(dsn, pool_pre_ping=True)
    cols = None

    with eng.begin() as cx:
        for batch in _chunks(rows, 1000):
            if cols is None:
                cols = list(batch[0].keys())
                
            placeholders = ", ".join(f":{c}" for c in cols)
            updates = ",".join(f"{c}=EXCLUDED.{c}" for c in cols if c not in key_cols)
            sql = f"""
            INSERT INTO {table} ({', '.join(cols)})
            VALUES ({placeholders})
            ON CONFLICT ({', '.join(key_cols)}) DO UPDATE SET {updates}
            """
            
            cx.execute(text(sql), batch)