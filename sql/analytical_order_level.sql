-- Monthly Revenue
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(order_revenue)::numeric, 2) AS monthly_revenue
FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp::timestamp)
ORDER BY month;

-- Top 10 Product Categories
SELECT
    product_categories AS product_category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(order_revenue)::numeric, 2) AS total_revenue
FROM analytical_order_level
WHERE order_status = 'delivered'
  AND product_categories IS NOT NULL
GROUP BY product_categories
ORDER BY total_revenue DESC
LIMIT 10;

-- Average Order Value
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_order_value)::numeric, 2) AS total_revenue,
    ROUND(AVG(total_order_value)::numeric, 2) AS average_order_value
FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp::timestamp)
ORDER BY month;

-- Late Delivery Analysis
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(order_revenue)::numeric, 2) AS monthly_revenue
FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp::timestamp)
ORDER BY month;

-- Top 10 Products Categories
SELECT
    COUNT(*) AS total_delivered_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'Late'
    ) AS late_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'Early'
    ) AS early_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'On Time'
    ) AS on_time_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE delivery_status = 'Late'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_percentage

FROM analytical_order_level
WHERE is_delivered = TRUE;

-- Customer Revenue Ranking
SELECT
    customer_unique_id,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_order_value)::numeric, 2) AS total_revenue,

    RANK() OVER (
        ORDER BY SUM(total_order_value) DESC
    ) AS revenue_rank

FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY customer_unique_id
ORDER BY revenue_rank
LIMIT 20;

-- Repeat Customers
SELECT
    COUNT(*) AS repeat_customers
FROM (
    SELECT
        customer_unique_id
    FROM analytical_order_level
    WHERE order_status = 'delivered'
    GROUP BY customer_unique_id
    HAVING COUNT(DISTINCT order_id) > 1
) AS customers;

-- Repeat Customers with Revenue
SELECT
    customer_unique_id,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_order_value)::numeric, 2) AS total_revenue,
    ROUND(AVG(total_order_value)::numeric, 2) AS average_order_value
FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY customer_unique_id
HAVING COUNT(DISTINCT order_id) > 1
ORDER BY total_revenue DESC;

-- Complete Customer Segmentation
WITH customer_metrics AS (
    SELECT
        customer_unique_id,

        COUNT(DISTINCT order_id) AS total_orders,

        SUM(total_order_value) AS total_revenue,

        AVG(total_order_value) AS average_order_value

    FROM analytical_order_level

    WHERE order_status = 'delivered'

    GROUP BY customer_unique_id
)

SELECT
    customer_unique_id,
    total_orders,

    ROUND(total_revenue::numeric, 2) AS total_revenue,

    ROUND(average_order_value::numeric, 2) AS average_order_value,

    CASE
        WHEN total_orders = 1 THEN 'One-Time Customer'
        WHEN total_orders BETWEEN 2 AND 3 THEN 'Repeat Customer'
        ELSE 'Loyal Customer'
    END AS customer_segment,

    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank

FROM customer_metrics

ORDER BY total_revenue DESC;