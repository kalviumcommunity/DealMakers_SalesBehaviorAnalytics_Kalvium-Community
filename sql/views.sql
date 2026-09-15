-- Reusable views joining opportunity_features to the supporting reference
-- tables (sales_teams, products). Executed by src/load_database.py every
-- time the database is rebuilt, so they always match the current data.

DROP VIEW IF EXISTS agent_team_performance;
CREATE VIEW agent_team_performance AS
SELECT
    st.regional_office,
    st.manager,
    o.sales_agent,
    COUNT(*) AS opportunities,
    SUM(o.is_closed) AS closed_opportunities,
    ROUND(100.0 * SUM(o.is_won) / NULLIF(SUM(o.is_closed), 0), 2) AS win_rate_pct,
    ROUND(AVG(o.deal_duration_days), 2) AS avg_deal_duration_days
FROM opportunity_features o
JOIN sales_teams st ON st.sales_agent = o.sales_agent
GROUP BY st.regional_office, st.manager, o.sales_agent;


-- LEFT JOIN, not INNER: opportunity_features.product includes "GTXPro"
-- (no space), which does not match products.product ("GTX Pro"). An INNER
-- JOIN would silently drop those opportunities; series/list_price are NULL
-- for them here instead, which is the honest representation of the mismatch.
DROP VIEW IF EXISTS product_line_performance;
CREATE VIEW product_line_performance AS
SELECT
    o.product,
    p.series,
    p.sales_price AS list_price,
    COUNT(*) AS opportunities,
    ROUND(100.0 * SUM(o.is_won) / NULLIF(SUM(o.is_closed), 0), 2) AS win_rate_pct,
    ROUND(AVG(CASE WHEN o.is_won = 1 THEN o.close_value END), 2) AS avg_won_close_value
FROM opportunity_features o
LEFT JOIN products p ON p.product = o.product
GROUP BY o.product, p.series, p.sales_price;
