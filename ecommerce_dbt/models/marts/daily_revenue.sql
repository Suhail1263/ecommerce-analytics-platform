SELECT
    d.full_date,
    d.year,
    d.month_name,
    d.is_weekend,
    s.store_name,
    s.city AS store_city,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_units_sold,
    SUM(f.total_amount) AS total_revenue,
    ROUND(AVG(f.total_amount), 2) AS avg_order_value
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_date') }} d ON f.date_id = d.date_id
JOIN {{ ref('dim_store') }} s ON f.store_id = s.store_id
WHERE f.order_status = 'COMPLETED'
GROUP BY d.full_date, d.year, d.month_name, d.is_weekend, s.store_name, s.city