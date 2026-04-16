/*
Simple staging area.
*/

select category,
    cast(date as date) as date,
    country,
    device,
    metric,
    value
from {{source('appstore','categories')}}