# Trend Acceleration Scoring (v1)

## Inputs

For each keyword `k`:
- `count_7d`
- `count_prev_7d`
- `share_7d`
- `share_prev_7d`

## Formula

- `growth_rate = (count_7d - count_prev_7d) / max(count_prev_7d, 1)`
- `share_delta = share_7d - share_prev_7d`
- `accel_score = 0.6 * growth_rate + 0.4 * share_delta`

## Filters

- Minimum volume: `count_7d >= 10`
- Winsorize top 1% outliers
- Report top 15 keywords weekly

## Output tables

- `gold_topic_daily_metrics`
- `gold_trend_acceleration`
