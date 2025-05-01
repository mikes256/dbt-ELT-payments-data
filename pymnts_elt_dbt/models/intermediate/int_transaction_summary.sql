select
    type
    , sum(amount) as total_amount
    , avg(amount) as average_amount
    , min(amount) as minimum_amount
    , max(amount) as maximum_amount
from {{ ref('fct_transation') }}
group by type
