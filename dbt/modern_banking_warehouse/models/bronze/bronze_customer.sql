{{ config(materialized='table') }}
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone_number,
    date_of_birth,
    address,
    status,
    created_at,
    updated_at
FROM {{ source('raw', 'customers') }}