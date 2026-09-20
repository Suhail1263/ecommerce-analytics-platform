select product_id,
trim(product_name) as product_name,
trim(category) as category,
unit_price
from {{source('raw','raw_products')}}
where product_id is not null