select date,
  device,
  rating_type,
  value
from {{ref('stg_ratings')}}
where app = '{{var("target_app")}}'