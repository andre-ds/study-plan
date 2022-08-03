
-- first purchase (first_value)
select
customer_unique_id,
price,
date,
first_value(date) over(partition by customer_unique_id order by date asc) as first_purchase
from dw.fact_sales
order by customer_unique_id

-- last purchase (last_value)
select
customer_unique_id,
price,
date,
first_value(date) over(partition by customer_unique_id order by date
rows between unbounded preceding and unbounded following) as last_purchase
from dw.fact_sales
order by customer_unique_id

-- next register, that is next purchase (lead)
select
customer_unique_id,
price,
date,
lead(date) over(partition by customer_unique_id order by date) as lead
from dw.fact_sales
order by customer_unique_id

-- lag
select
customer_unique_id,
price,
date,
lag(date) over(partition by customer_unique_id order by date) as lag
from dw.fact_sales
order by customer_unique_id

-- rank
select
customer_unique_id,
price,
date,
rank() over(partition by customer_unique_id order by date) as rank
from dw.fact_sales
order by customer_unique_id

-- row_number
select
customer_unique_id,
price,
date,
row_number() over(partition by customer_unique_id order by date) as row_number
from dw.fact_sales
order by customer_unique_id