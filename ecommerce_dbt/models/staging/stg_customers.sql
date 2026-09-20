select
customer_id,
trim(customer_name) as customer_name,
lower(trim(email)) as email,
trim(city) as city,
trim(country) as country,
signup_date
from {{source('raw','raw_customers')}}
where customer_id is not null