select date,
  country,
  device,
  category,
  store_type,
  rank
from {{ref("int_rankings")}}
where app = '{{var("target_app")}}'