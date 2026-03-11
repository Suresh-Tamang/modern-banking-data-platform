{{ config(materialized='table') }}
SELECT 
    account_id,
    count(transaction_id) as total_transactions,
    sum(amount) as total_transaction_amount
FROM {{ ref('silver_transaction') }}
GROUP BY account_id