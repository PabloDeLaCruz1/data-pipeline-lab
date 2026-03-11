with base as (
  select * from {{ ref('gold_topic_daily_metrics') }}
),
roll as (
  select
    published_date,
    keyword,
    theme,
    sum(mention_count) over (
      partition by keyword order by published_date
      rows between 6 preceding and current row
    ) as count_7d,
    sum(mention_count) over (
      partition by keyword order by published_date
      rows between 13 preceding and 7 preceding
    ) as count_prev_7d,
    avg(mention_share) over (
      partition by keyword order by published_date
      rows between 6 preceding and current row
    ) as share_7d,
    avg(mention_share) over (
      partition by keyword order by published_date
      rows between 13 preceding and 7 preceding
    ) as share_prev_7d
  from base
)
select
  published_date,
  keyword,
  theme,
  count_7d,
  count_prev_7d,
  share_7d,
  share_prev_7d,
  (count_7d - coalesce(count_prev_7d,0))::float / nullif(greatest(coalesce(count_prev_7d,0),1),0) as growth_rate,
  (share_7d - coalesce(share_prev_7d,0)) as share_delta,
  0.6 * ((count_7d - coalesce(count_prev_7d,0))::float / nullif(greatest(coalesce(count_prev_7d,0),1),0))
  + 0.4 * (share_7d - coalesce(share_prev_7d,0)) as accel_score
from roll
where count_7d >= 10
