select app,
  date,
  device,
  keyword,
  metric,
  effective_value
from {{ref('stg_keywords')}}
where country = 'us'