select
  app,
  date,
  device,
  metric,
  value,
  round(
    value / sum(value) over (
      partition by date, device, metric
    ),
    4
  ) as pct_total
from {{ref('stg_metrics')}}
where country = '{{var("target_country")}}'
