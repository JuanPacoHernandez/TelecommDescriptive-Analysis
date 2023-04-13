{{config(
    materialized='table',
    partition_by = {
        "field":"year_of_birth",
        "data_type":"int64",
        "range":{
            "start":1943,
            "end":2015,
            "interval":9
        }
    },
    cluster_by = "gender"
)}}

SELECT * FROM {{ ref('stg_crm') }}

