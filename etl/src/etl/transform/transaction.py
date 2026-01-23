from typing import Iterable, Iterator
from ...models import Transaction

def transform_transactions(raw_transactions: Iterable[dict]) -> Iterator[Transaction]:
    for raw in raw_transactions:
        yield Transaction(
            transcation_id=raw['transaction_id'],
            account_id=raw['account_id'],
            transaction_type=raw['transaction_type'],
            amount=float(raw['amount']),
            transaction_date=raw['transaction_date'],
            created_at=raw['created_at'],
            updated_at=raw['updated_at']
        )