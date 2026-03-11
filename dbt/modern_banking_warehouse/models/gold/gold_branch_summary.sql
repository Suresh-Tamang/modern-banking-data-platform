{{ config(materialized='table') }}
SELECT
    b.branch_id,
    b.branch_name,
    COUNT(a.account_id) as total_accounts,
    SUM(a.balance) as branch_total_balancee
FROM {{ ref('silver_branch') }} b
LEFT JOIN {{ ref('silver_account') }} a
ON b.branch_id = a.branch_id
GROUP BY
    b.branch_id,
    b.branch_name