{% snapshot customer_snapshot %}
{{ config(
    target_schema='snapshots',
    unique_key='customer_id',
    strategy='check',
    check_cols=['first_name', 'last_name', 'email', 'status'],
    invalidated_hard_deletes=True
    )
}}
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    phone_number,
    date_of_birth,
    address,
    status,
    updated_at
FROM {{ ref('bronze_customer') }}
{% endsnapshot %}