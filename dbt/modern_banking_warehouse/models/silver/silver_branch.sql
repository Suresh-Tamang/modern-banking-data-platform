{{ config(materialized='table') }}
select 
    branch_id,
    branch_name,
    location,
    manager_name,
    created_at
from {{ ref('bronze_branch') }}