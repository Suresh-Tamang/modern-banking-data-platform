{{ config(materialized='table') }}
SELECT
    branch_id,
    branch_name,
    location,
    manager_name,
    created_at,
    updated_at
FROM {{ source('raw', 'branches') }}