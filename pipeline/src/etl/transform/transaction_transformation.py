from typing import Iterable
import pandas as pd
from ...models import Transaction


def transform_transactions(raw_transactions: Iterable[dict]) -> pd.DataFrame:
    transformed = []

    for raw in raw_transactions:
        transaction = Transaction(**raw)  # validation happens here
        transformed.append(transaction.model_dump())

    return pd.DataFrame(transformed)
