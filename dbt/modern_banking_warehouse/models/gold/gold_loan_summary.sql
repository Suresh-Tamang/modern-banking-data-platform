{{ config(materialized='table') }}
SELECT
    branch_id,
    count(loan_id) as total_loans,
    sum(loan_amount) as total_loan_amount
FROM {{ ref('silver_loan') }}
GROUP BY branch_id