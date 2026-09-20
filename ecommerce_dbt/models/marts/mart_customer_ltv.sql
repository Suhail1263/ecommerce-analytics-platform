SELECT
    c.customer_id,
    c.customer_name,
    c.country,
    c.signup_date,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.total_amount) AS lifetime_value,
    ROUND(AVG(f.total_amount), 2) AS avg_order_value,
    MAX(d.full_date) AS last_order_date
FROM {{ ref('dim_customer') }} c
LEFT JOIN {{ ref('fact_sales') }} f ON c.customer_id = f.customer_id AND f.order_status = 'COMPLETED'
LEFT JOIN {{ ref('dim_date') }} d ON f.date_id = d.date_id
GROUP BY c.customer_id, c.customer_name, c.country, c.signup_date