{{ config(materialized='table') }}
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(a.account_id) AS total_accounts,
    SUM(a.balance) AS total_balance
FROM {{ ref('silver_customer') }} c
LEFT JOIN {{ ref('silver_account') }} a
ON c.customer_id = a.customer_id
GROUP BY 
    c.customer_id,
    c.first_name,
    c.last_name