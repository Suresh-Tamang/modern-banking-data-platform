{{ config(materialized='table') }}

SELECT

    account_id,

    COUNT(transaction_id) AS transaction_count,

    SUM(amount) AS total_amount,

    AVG(amount) AS avg_transaction_amount,

    MAX(amount) AS max_transaction,

    MIN(amount) AS min_transaction,

    COUNT(
        CASE
            WHEN transaction_type = 'debit'
            THEN 1
        END
    ) AS withdrawal_count,

    COUNT(
        CASE
            WHEN transaction_type = 'credit'
            THEN 1
        END
    ) AS deposit_count

FROM {{ ref('silver_transaction') }}

GROUP BY account_id