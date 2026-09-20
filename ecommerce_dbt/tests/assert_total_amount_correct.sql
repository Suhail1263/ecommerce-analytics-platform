SELECT
    order_id,
    quantity,
    unit_price,
    total_amount
FROM {{ ref('fact_sales') }}
WHERE ROUND(quantity * unit_price, 2) != ROUND(total_amount, 2)