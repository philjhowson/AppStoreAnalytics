select app,
  date,
  device,
  value
from {{ref('stg_ratings')}}
where country = 'us'
  and rating_type = 'avg_rating'