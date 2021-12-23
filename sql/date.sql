-- Obtendo Data Atual
SELECT
current_date AS time_1,
current_time AS time_2,
current_timestamp as time_3;

-- Filtrando a data exata
select *
from olist.orders
where order_purchase_timestamp = '2017-10-02 10:56:33'

-- Filtrando baseada em operadores lógicos
select *
from olist.orders
where order_purchase_timestamp > '2017-10-02 '

-- Filtrando entre determinada data (Between)
select *
from olist.orders
where order_purchase_timestamp between '2017-09-01' and '2017-10-01'

-- Extraindo ano, mes, dia e hora
select
order_purchase_timestamp,
extract(year from order_purchase_timestamp) as year,
extract(month from order_purchase_timestamp) as month,
extract(day from order_purchase_timestamp) as day,
extract(hour from order_purchase_timestamp) as hour
from olist.orders

-- Filtrando com extract
select *
from olist.orders
where extract(year from order_purchase_timestamp) = 2017

-- Transforming date
select
order_purchase_timestamp,
date(order_purchase_timestamp) as test_1
from olist.orders

-- Transformando data diretamente a partir do select
select
order_purchase_timestamp,
order_purchase_timestamp::date as test_1,
order_purchase_timestamp::timestamp as test_2,
order_purchase_timestamp::time as test_3
from olist.orders

-- Definindo time zone
select
order_purchase_timestamp,
extract(hour from order_purchase_timestamp at time zone 'America/Sao_Paulo') as hour
from olist.orders

-- Adicionando a hora, dia, mes, ano a data
select 
order_purchase_timestamp,
order_purchase_timestamp + INTERVAL '1 hour' as time_1,
order_purchase_timestamp + INTERVAL '1 day' as time_2,
order_purchase_timestamp + INTERVAL '1 month' as time_3,
order_purchase_timestamp + INTERVAL '1 year' as time_4
from olist.orders;

-- Removendo a hora, dia, mes, ano a data
select 
order_purchase_timestamp,
order_purchase_timestamp - INTERVAL '1 hour' as time_1,
order_purchase_timestamp - INTERVAL '1 day' as time_2,
order_purchase_timestamp - INTERVAL '1 month' as time_3,
order_purchase_timestamp - INTERVAL '1 year' as time_4
from olist.orders;