/*
Simple staging area.
*/

select app,
    cast(date as date) as date,
    country,
    device,
    category_name as category,
    chart_type as store_type,
    rank,
    fetch_depth as depth
from {{source('appstore','category_ranking')}}