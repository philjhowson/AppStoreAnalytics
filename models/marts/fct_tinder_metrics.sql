select date,
  country,
  device,
  metric,
  value
from {{ref('stg_metrics')}}
where app = '{{var("target_app")}}'