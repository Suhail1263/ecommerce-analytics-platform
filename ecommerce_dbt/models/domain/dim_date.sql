WITH date_spine AS (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2023-01-01' as date)",
        end_date="cast('2027-12-31' as date)"
    ) }}
)

SELECT
    TO_NUMBER(TO_CHAR(date_day, 'YYYYMMDD')) AS date_id,
    date_day AS full_date,
    YEAR(date_day) AS year,
    MONTH(date_day) AS month,
    DAY(date_day) AS day,
    MONTHNAME(date_day) AS month_name,
    DAYNAME(date_day) AS day_name,
    QUARTER(date_day) AS quarter,
    CASE WHEN DAYOFWEEK(date_day) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_spine