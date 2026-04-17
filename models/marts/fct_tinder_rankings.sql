select date,
  country,
  device,
  category,
  store_type,
  rank
from {{ref("stg_category_ranking")}}
where app = '{{var("target_app")}}'
  and (category = 'all'
    or category = 'dating'
    or category = 'lifestyle')