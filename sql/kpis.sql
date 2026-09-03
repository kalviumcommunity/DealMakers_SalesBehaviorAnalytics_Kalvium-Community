-- Total opportunities
SELECT COUNT(*) AS total_opportunities
FROM opportunity_features;


-- Closed opportunities
SELECT COUNT(*) AS closed_opportunities
FROM opportunity_features
WHERE is_closed = 1;


-- Win rate
SELECT
    ROUND(
        100.0 * SUM(is_won) /
        NULLIF(SUM(is_closed), 0),
        2
    ) AS win_rate
FROM opportunity_features;


-- Average deal duration
SELECT
    ROUND(
        AVG(deal_duration_days),
        2
    ) AS avg_deal_duration_days
FROM opportunity_features
WHERE is_closed = 1;


-- Average deal value
SELECT
    ROUND(
        AVG(close_value),
        2
    ) AS avg_close_value
FROM opportunity_features
WHERE is_closed = 1;


-- Performance by sales agent
SELECT
    sales_agent,
    COUNT(*) AS opportunities,
    ROUND(
        100.0 * SUM(is_won) /
        NULLIF(SUM(is_closed), 0),
        2
    ) AS win_rate,
    ROUND(
        AVG(deal_duration_days),
        2
    ) AS avg_deal_duration,
    ROUND(
        AVG(response_rate),
        3
    ) AS avg_response_rate
FROM opportunity_features
GROUP BY sales_agent
ORDER BY avg_deal_duration ASC;


-- Behaviour by deal speed
SELECT
    deal_speed,
    COUNT(*) AS opportunities,
    ROUND(AVG(response_rate), 3)
        AS avg_response_rate,
    ROUND(AVG(avg_response_time_hours), 2)
        AS avg_response_time_hours,
    ROUND(AVG(activity_count), 2)
        AS avg_activity_count,
    ROUND(AVG(followup_count), 2)
        AS avg_followup_count
FROM opportunity_features
WHERE is_closed = 1
GROUP BY deal_speed
ORDER BY
    CASE deal_speed
        WHEN 'Fast' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Slow' THEN 3
    END;


-- Pipeline funnel
SELECT
    deal_stage,
    COUNT(*) AS opportunities
FROM opportunity_features
GROUP BY deal_stage
ORDER BY opportunities DESC;


-- Won versus Lost behavioural comparison (closed opportunities only)
SELECT
    deal_stage AS outcome,
    COUNT(*) AS opportunities,
    ROUND(AVG(response_rate) * 100, 2) AS avg_response_rate_pct,
    ROUND(AVG(avg_response_time_hours), 2) AS avg_response_time_hours,
    ROUND(AVG(activity_count), 2) AS avg_activity_count,
    ROUND(AVG(stage_transition_count), 2) AS avg_stage_transitions,
    ROUND(AVG(deal_duration_days), 2) AS avg_deal_duration_days
FROM opportunity_features
WHERE is_closed = 1
GROUP BY deal_stage
ORDER BY outcome;


-- Win rate by descriptive engagement level
SELECT
    engagement_level,
    COUNT(*) AS opportunities,
    SUM(is_closed) AS closed_opportunities,
    ROUND(100.0 * SUM(is_won) / NULLIF(SUM(is_closed), 0), 2) AS win_rate_pct,
    ROUND(AVG(activity_count), 2) AS avg_activity_count,
    ROUND(AVG(response_rate) * 100, 2) AS avg_response_rate_pct
FROM opportunity_features
GROUP BY engagement_level
ORDER BY CASE engagement_level
    WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 ELSE 4 END;


-- Win rate by email response-rate band
SELECT
    CASE
        WHEN has_behavioural_history = 0 THEN 'No history'
        WHEN response_rate < 0.35 THEN 'Low (<35%)'
        WHEN response_rate < 0.60 THEN 'Medium (35-59%)'
        ELSE 'High (60%+)'
    END AS response_rate_band,
    COUNT(*) AS opportunities,
    ROUND(100.0 * SUM(is_won) / NULLIF(SUM(is_closed), 0), 2) AS win_rate_pct,
    ROUND(AVG(deal_duration_days), 2) AS avg_deal_duration_days
FROM opportunity_features
GROUP BY response_rate_band
ORDER BY CASE response_rate_band
    WHEN 'High (60%+)' THEN 1 WHEN 'Medium (35-59%)' THEN 2
    WHEN 'Low (<35%)' THEN 3 ELSE 4 END;


-- Sales-agent behavioural and outcome comparison
SELECT
    sales_agent,
    COUNT(*) AS opportunities,
    ROUND(100.0 * SUM(is_won) / NULLIF(SUM(is_closed), 0), 2) AS win_rate_pct,
    ROUND(AVG(response_rate) * 100, 2) AS avg_response_rate_pct,
    ROUND(AVG(activity_count), 2) AS avg_activity_count,
    ROUND(AVG(deal_duration_days), 2) AS avg_deal_duration_days
FROM opportunity_features
GROUP BY sales_agent
ORDER BY win_rate_pct DESC, opportunities DESC;


-- Product outcome and behavioural comparison
SELECT
    product,
    COUNT(*) AS opportunities,
    ROUND(100.0 * SUM(is_won) / NULLIF(SUM(is_closed), 0), 2) AS win_rate_pct,
    ROUND(AVG(response_rate) * 100, 2) AS avg_response_rate_pct,
    ROUND(AVG(activity_count), 2) AS avg_activity_count,
    ROUND(AVG(deal_duration_days), 2) AS avg_deal_duration_days
FROM opportunity_features
GROUP BY product
ORDER BY opportunities DESC;
