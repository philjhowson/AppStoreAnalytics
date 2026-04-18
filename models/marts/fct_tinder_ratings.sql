with totals as (
    select date,
      country,
      device, 
      value as total_ratings
    from {{ref('stg_ratings')}}
    where rating_type = 'rating_total'
)

select r.date,
  r.country,
  r.device,
  r.rating_type,
  r.value,
  case when r.rating_type != 'avg_rating' then r.value / t.total_ratings else NULL end as pct_ratings
  from {{ref('stg_ratings')}} r
join totals t
  using (date, country, device)
where r.rating_type != 'total_rating'
    and r.app = '{{var("target_app")}}'