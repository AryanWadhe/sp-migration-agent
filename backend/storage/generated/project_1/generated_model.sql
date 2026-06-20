with

usp_update_statistic_source as (

    select *
    from {{ source('legacy', 'usp_update_statistic') }}

)


select *
from usp_update_statistic_source