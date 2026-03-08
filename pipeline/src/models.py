from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class Transaction(BaseModel):
    transaction_id: str = Field(...,
                                description="Unique identifier for the transaction")
    account_id: str = Field(...,
                            description="Unique identifier for the transaction", validation_alias='account')
    transaction_type: str = Field(
        ..., description="Type of the transaction, e.g., 'debit', 'credit'")
    amount: float = Field(..., description="Amount of the transaction")
    description: str = Field(
        "", description="Optional description of the transaction")
    transaction_date: str = Field(...,
                                  description="Date of the transaction in ISO format")
    created_at: str = Field(..., description="Timestamp when the transaction was created in ISO format")
    updated_at: str = Field(
        ..., description="Timestamp when the transaction was last updated in ISO format")

    @field_validator('transaction_id', 'transaction_type', 'transaction_date', 'created_at', 'updated_at')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field must not be empty')
        return v

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Amount must be non-negative')
        return v
    

class CustomerSchema(BaseModel):
    customer_id: str = Field(...,
                             description="Unique identifier for the customer")
    first_name: str = Field(..., description="Customer's first name")
    last_name: str = Field(..., description="Customer's last name")
    email: str = Field(..., description="Unique email address")
    phone_number: str = Field(..., description="Contact phone number")
    date_of_birth: date = Field(..., description="Customer date of birth")
    address: str = Field(..., description="Physical address")
    status: str = Field("active", description="Account status")
    created_at: str = Field(..., description="ISO creation timestamp")
    updated_at: str = Field(..., description="ISO update timestamp")

    @field_validator('customer_id', 'first_name', 'last_name', 'email', 'status')
    @classmethod
    def not_empty(cls, v):
        if not v or not str(v).strip():
            raise ValueError('Field must not be empty')
        return v


class BranchSchema(BaseModel):
    branch_id: str = Field(..., description="Unique branch identifier")
    branch_name: str = Field(..., description="Name of the bank branch")
    location: str = Field(..., description="Physical location/city")
    manager_name: str = Field(..., description="Name of the branch manager")
    created_at: str = Field(..., description="ISO creation timestamp")
    updated_at: str = Field(..., description="ISO creation timestamp")
    @field_validator('branch_id', 'branch_name', 'location')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field must not be empty')
        return v
    

class AccountSchema(BaseModel):
    account_id: str = Field(..., description="Unique account identifier")
    account_type: str=Field("Savings", description="Types of account")
    balance: float = Field(0.00, description="Current ledger balance")
    status: str = Field("active", description="Account status")
    opened_date: date = Field(..., description="Timestamp when the account was created in ISO format")
    created_at: str = Field(..., description="Timestamp when the transaction was created in ISO format")
    updated_at: str =  Field(..., description="Timestamp when the transaction was updated in ISO format")
    customer: str = Field(..., description="unique customer identifier")
    branch: str = Field(..., description="unique branch identifier")
    

    @field_validator('account_id', 'status')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field must not be empty')
        return v

    @field_validator('balance')
    @classmethod
    def validate_balance(cls, v):
        if v < 0:
            raise ValueError('Balance cannot be negative')
        return v



class LoanSchema(BaseModel):
    loan_id: str = Field(..., description="Unique loan identifier")
    loan_amount: float = Field(..., description="Total principal amount")
    interest_rate: float = Field(...,
                                 description="Annual interest rate percentage")
    start_date: date
    end_date: date
    status: str = Field("pending", description="Current loan status")
    created_at: str
    updated_at: str
    customer: str = Field(..., description="unique customer identifier")
    branch: str = Field(..., description="unique branch identifier")

    @field_validator('loan_id', 'status')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field must not be empty')
        return v

    @field_validator('loan_amount', 'interest_rate')
    @classmethod
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v

