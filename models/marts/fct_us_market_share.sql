with category_totals as (
  select category,
    date,
    device,
    metric,
    value
  from {{ref('stg_categories')}}
where country = '{{var("target_country")}}'
    and (
      (device = 'android' and category = 'dating')
      or
      (device = 'iphone' and category = 'lifestyle')
    )
)

select m.app,
  m.date,
  m.device,
  m.metric,
  m.value,
  round(m.value / c.value, 4) as pct_total
from {{ref('stg_metrics')}} m
join category_totals c
  using(date, device, metric)
where country = '{{var("target_country")}}'