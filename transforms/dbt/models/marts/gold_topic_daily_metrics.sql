with mentions as (
  select * from {{ ref('int_keyword_mentions') }} where mentioned = 1
),
daily_counts as (
  select
    published_date,
    keyword,
    theme,
    count(*) as mention_count
  from mentions
  group by 1,2,3
),
daily_totals as (
  select
    published_date,
    count(distinct paper_id) as total_papers
  from {{ ref('stg_arxiv_papers') }}
  group by 1
)
select
  d.published_date,
  d.keyword,
  d.theme,
  d.mention_count,
  t.total_papers,
  d.mention_count::float / nullif(t.total_papers, 0) as mention_share
from daily_counts d
join daily_totals t using (published_date)
