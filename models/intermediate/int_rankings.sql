select app,
  date,
  country,
  device,
  category,
  store_type,
  rank
from {{ref("stg_category_ranking")}}
where category = 'all'
    or category = 'dating'
    or category = 'lifestyle'