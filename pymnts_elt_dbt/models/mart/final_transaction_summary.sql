
SELECT
    type,
    total_amount,
    minimum_amount,
    maximum_amount,
    (maximum_amount - minimum_amount) as range
FROM {{ ref('int_transaction_summary') }}
