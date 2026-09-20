SELECT
    order_id,
    customer_id,
    product_id,
    store_id,
    order_timestamp,
    CAST(order_timestamp AS DATE) AS order_date,
    quantity,
    UPPER(TRIM(order_status)) AS order_status
FROM {{ source('raw', 'raw_orders') }}
WHERE order_id IS NOT NULL
  AND quantity > 0