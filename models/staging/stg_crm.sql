{{ config(materialized='view') }}

select 
    msisdn,
    gender,
    year_of_birth,
    system_status,
    mobile_type,
    value_segment

from {{ source('staging', 'external_CRM') }}
    