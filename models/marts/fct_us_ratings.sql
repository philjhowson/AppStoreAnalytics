select app,
  date,
  device,
  value
from {{ref('stg_ratings')}}
where country = '{{var("target_country")}}'
  and rating_type = 'avg_rating'