-- Assumes bronze_arxiv_raw exists with columns:
-- paper_id, published_at, title, abstract, categories

select
  paper_id,
  cast(published_at as timestamp) as published_at,
  lower(coalesce(title, '')) as title,
  lower(coalesce(abstract, '')) as abstract,
  lower(coalesce(categories, '')) as categories
from public.bronze_arxiv_raw
