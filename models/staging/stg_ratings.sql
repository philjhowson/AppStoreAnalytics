/*
Simple staging area. Unpivots the columns to create
long format for better scalability.
*/

select
  app,
  cast(date as date) as date,
  country,
  device,
  rating_type,
  value
from {{ source('appstore', 'ratings') }}

unpivot (
  value for rating_type in (
    rating_1,
    rating_2,
    rating_3,
    rating_4,
    rating_5,
    avg_rating,
    rating_total
  )
)