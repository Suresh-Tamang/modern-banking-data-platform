{{ config(
    materialized='incremental',
    unique_key='transaction_id'
) }}

select
    transaction_id,
    account_id,
    transaction_type,
    amount,
    transaction_date
from {{ ref('bronze_transaction') }}
where amount > 0

{% if is_incremental() %}
    and transaction_date > (select max(transaction_date) from {{ this }})
{% endif %}