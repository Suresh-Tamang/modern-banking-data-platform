from typing import Iterable, Iterator
from ...models import Transaction, CustomerSchema, BranchSchema, LoanSchema, AccountSchema

def normalize_transactions(rows: Iterable[dict]) -> Iterator[Transaction]:
    for row in rows:
        yield Transaction(**row)
        
        
def normalize_accounts(rows: Iterable[dict]) -> Iterator[AccountSchema]:
    for row in rows:
        yield AccountSchema(**row)


def normalize_customers(rows: Iterable[dict]) -> Iterator[CustomerSchema]:
    for row in rows:
        yield CustomerSchema(**row)


def normalize_branches(rows: Iterable[dict]) -> Iterator[BranchSchema]:
    for row in rows:
        yield BranchSchema(**row)


def normalize_loans(rows: Iterable[dict]) -> Iterator[LoanSchema]:
    for row in rows:
        yield LoanSchema(**row)
