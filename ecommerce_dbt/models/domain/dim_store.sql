SELECT
    store_id,
    store_name,
    city,
    country
FROM {{ ref('stg_stores') }}