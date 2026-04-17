select app,
  date,
  category,
  device,
  rank
from {{ref('stg_category_ranking')}}
where country = 'us'
  and (
    category = 'dating'
    or category = 'all'
    or category = 'lifestyle'
  )