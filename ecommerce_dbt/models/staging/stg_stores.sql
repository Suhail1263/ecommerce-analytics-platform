SELECT
    store_id,
    TRIM(store_name) AS store_name,
    TRIM(city) AS city,
    TRIM(country) AS country
FROM {{ source('raw', 'raw_stores') }}
WHERE store_id IS NOT NULL