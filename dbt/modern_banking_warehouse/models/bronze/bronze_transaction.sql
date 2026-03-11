{{ config(materialized='table') }}
SELECT
    transaction_id,
    account_id,
    transaction_type,
    amount,
    description,
    transaction_date,
    created_at,
    updated_at
FROM {{ source('raw', 'transactions') }}