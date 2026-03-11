{{ config(materialized='table') }}
SELECT 
    account_id,
    account_type,
    balance,
    status,
    opened_date,
    created_at,
    updated_at,
    customer_id,
    branch_id
FROM {{ source('raw', 'accounts') }}