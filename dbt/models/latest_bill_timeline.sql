with latest_with_history AS (
    SELECT 
        lbol.bill_type,
        lbol.submit_diet_no,
        lbol.submit_bill_no,
        lbol.status,
        lbol.representatives_deliveration_result,
        lbol.councilors_deliveration_result,
        lh.first_representatives_accept_date,
        lh.last_representatives_finish_date,
        lh.first_councilors_accept_date,
        lh.last_councilors_finish_date,
        lbol.promulgation_date
    FROM {{ ref('latest_bill_of_lows') }} as lbol
    JOIN {{ ref('low_history') }} as lh USING (bill_type, submit_diet_no, submit_bill_no) 
),
representatives_finished AS (
    SELECT 
        bill_type,
        submit_diet_no, 
        submit_bill_no,
        first_representatives_accept_date AS start_date,
        last_representatives_finish_date AS end_date,
        CONCAT("衆議院で審議", " → ", representatives_deliveration_result) AS status
    FROM 
        latest_with_history
    WHERE 
        first_representatives_accept_date IS NOT NULL
        AND last_representatives_finish_date IS NOT NULL
),
representatives_in_progress AS (
   SELECT 
        bill_type,
        submit_diet_no, 
        submit_bill_no,
        first_representatives_accept_date AS start_date,
        CURRENT_DATE("Asia/Tokyo") AS end_date,
        "衆議院で審議中" AS status
    FROM 
        latest_with_history
    WHERE 
        first_representatives_accept_date IS NOT NULL
        AND status = "衆議院で審議中"
),
councilors_finished AS (
    SELECT 
        bill_type,
        submit_diet_no, 
        submit_bill_no,
        first_councilors_accept_date AS start_date,
        last_councilors_finish_date AS end_date,
        CONCAT("参議院で審議", " → ", councilors_deliveration_result) AS status
    FROM 
        latest_with_history
    WHERE 
        first_councilors_accept_date IS NOT NULL
        AND last_councilors_finish_date IS NOT NULL
),
councilors_in_progress AS (
   SELECT 
        bill_type,
        submit_diet_no, 
        submit_bill_no,
        first_councilors_accept_date AS start_date,
        CURRENT_DATE("Asia/Tokyo") AS end_date,
        "参議院で審議中" AS status
    FROM 
        latest_with_history
    WHERE 
        first_councilors_accept_date IS NOT NULL
        AND status = "参議院で審議中"
),
established AS (
   SELECT 
        bill_type,
        submit_diet_no, 
        submit_bill_no,
        GREATEST(last_representatives_finish_date, last_councilors_finish_date) AS start_date,
        promulgation_date AS end_date,
        "成立 → 公布" AS status
    FROM 
        latest_with_history
    WHERE 
        status = "成立"
        AND promulgation_date IS NOT NULL
)

SELECT * 
FROM representatives_finished
UNION ALL
SELECT * 
FROM representatives_in_progress
UNION ALL
SELECT * 
FROM councilors_finished
UNION ALL
SELECT * 
FROM councilors_in_progress
UNION ALL
SELECT * 
FROM established