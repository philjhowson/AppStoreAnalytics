/*
Simple staging area.
*/

select app,
    cast(date as date) as date,
    country,
    device,
    keyword,
    metric,
    value,
    effective_value
from {{source('appstore','keywords')}}