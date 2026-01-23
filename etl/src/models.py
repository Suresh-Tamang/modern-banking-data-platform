from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Transaction(BaseModel):
    transcation_id: str = Field(..., description="Unique identifier for the transaction")
    account_id: str = Field(..., description="Unique identifier for the transaction")
    transaction_type: str = Field(..., description="Type of the transaction, e.g., 'debit', 'credit'")
    amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction in ISO format")
    created_at: str = Field(..., description="Timestamp when the transaction was created in ISO format")
    updated_at: str = Field(..., description="Timestamp when the transaction was last updated in ISO format")

    
    @field_validator('amount')
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Amount must be non-negative')
        return v