# Dashboard Spec (v1)

## Chart A: Top Rising Keywords (7d vs prev 7d)
- Source: `gold_trend_acceleration`
- Metric: `accel_score`
- Filter: latest `published_date`
- Limit: top 15

## Chart B: Theme Momentum Over Time
- Source: `gold_topic_daily_metrics`
- Metric: sum(`mention_share`) by `theme` and week
- Visualization: stacked area

## Chart C: Early Signal Tracker
- Source: `gold_trend_acceleration`
- Columns: keyword, theme, accel_score, count_7d, share_7d
- Sort: accel_score desc
