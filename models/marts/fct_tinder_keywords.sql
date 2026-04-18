select date,
  country,
  device,
  keyword,
  metric,
  value,
  effective_value
from {{ref('stg_keywords')}}
where app = '{{var("target_app")}}'