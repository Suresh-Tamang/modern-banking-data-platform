{{ config(materialized='table') }}

SELECT
    loan_id,
    customer_id,
    branch_id,
    loan_amount,
    interest_rate,
    start_date,
    end_date,
    status
FROM {{ ref('bronze_loan') }}