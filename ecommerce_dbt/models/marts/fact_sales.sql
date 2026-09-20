SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.store_id,
    TO_NUMBER(TO_CHAR(o.order_date, 'YYYYMMDD')) AS date_id,
    o.quantity,
    p.unit_price,
    ROUND(o.quantity * p.unit_price, 2) AS total_amount,
    o.order_status
FROM {{ ref('stg_orders') }} o
INNER JOIN {{ ref('dim_customer') }} c ON o.customer_id = c.customer_id
INNER JOIN {{ ref('dim_product') }} p ON o.product_id = p.product_id
INNER JOIN {{ ref('dim_store') }} s ON o.store_id = s.store_id
INNER JOIN {{ ref('dim_date') }} d ON TO_NUMBER(TO_CHAR(o.order_date, 'YYYYMMDD')) = d.date_id