select app,
  date,
  device,
  category,
  store_type,
  rank
from {{ref("int_rankings")}}
where country = '{{var("target_country")}}'
