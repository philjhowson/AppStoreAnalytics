select
    date,
    country,
    device,
    rating_type,
    value,

    case 
        when rating_type != 'avg_rating'
        then value / sum(value) over (
            partition by date, country, device
        )
    end as pct_ratings

from {{ref('stg_ratings')}}
where rating_type != 'rating_total'
  and app = '{{var("target_app")}}'
