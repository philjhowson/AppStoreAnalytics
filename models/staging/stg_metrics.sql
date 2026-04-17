/*
Simple staging area.
*/

select
  app,
  cast(date as date) as date,
  country,
  device,
  metric,
  value,
  precision
from {{ source('appstore', 'metrics') }}