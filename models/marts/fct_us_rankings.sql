select app,
  date,
  category,
  device,
  rank
from {{ref('stg_category_ranking')}}
where country = '{{var("target_country")}}'
  and (
    category = 'dating'
    or category = 'all'
    or category = 'lifestyle'
  )