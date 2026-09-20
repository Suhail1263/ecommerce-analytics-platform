SELECT
    session_id,
    customer_id,
    session_timestamp,
    CAST(session_timestamp AS DATE) AS session_date,
    TRIM(device_type) AS device_type,
    pages_viewed,
    session_duration_seconds
FROM {{ source('raw', 'raw_sessions') }}
WHERE session_id IS NOT NULL