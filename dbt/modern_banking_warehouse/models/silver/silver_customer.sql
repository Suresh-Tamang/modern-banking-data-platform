{{ config(materialized='table') }}
select 
    customer_id,
    INITCAP(first_name) AS first_name,
    INITCAP(last_name) AS last_name,
    LOWER(email) AS email,
    phone_number,
    date_of_birth,
    address,
    status,
    created_at,
    updated_at
FROM {{ ref('bronze_customer') }}
where status != 'inactive'