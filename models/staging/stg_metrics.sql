/*
Simple staging area.
*/

select app,
    cast(date as date) as date,
    country,
    device,
    metric,
    value
from {{source('appstore','metrics')}}
where precision >= 0.7