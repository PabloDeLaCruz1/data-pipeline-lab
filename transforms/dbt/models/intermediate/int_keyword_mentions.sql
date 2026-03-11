-- v1 keyword mention extraction scaffold
-- Replace inline keywords with YAML-driven generation in v2.

with base as (
  select * from {{ ref('stg_arxiv_papers') }}
),
keywords as (
  select 'transformer' as keyword, 'foundation_models' as theme union all
  select 'rag', 'retrieval_knowledge' union all
  select 'agent', 'agentic_systems' union all
  select 'multimodal', 'multimodal' union all
  select 'quantization', 'efficiency_infra' union all
  select 'alignment', 'safety_governance'
)
select
  b.paper_id,
  date_trunc('day', b.published_at)::date as published_date,
  k.keyword,
  k.theme,
  case
    when b.title like '%' || k.keyword || '%' then 1
    when b.abstract like '%' || k.keyword || '%' then 1
    else 0
  end as mentioned
from base b
cross join keywords k
