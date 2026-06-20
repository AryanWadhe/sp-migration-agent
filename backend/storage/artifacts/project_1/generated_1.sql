with

employee_source as (

    select *
    from {{ source('legacy', 'employee') }}

)
,

labor_source as (

    select *
    from {{ source('legacy', 'labor') }}

)


select *
from employee_source