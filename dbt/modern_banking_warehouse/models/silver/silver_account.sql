{{ config(materialized='table') }}

SELECT
    account_id,
    customer_id,
    branch_id,
    account_type,
    balance,
    status,
    opened_date
FROM {{ ref('bronze_account') }}
WHERE status = 'active'