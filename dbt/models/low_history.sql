SELECT bill_type,
    submit_diet_no,
    submit_bill_no,
    MIN(bill_subject) as bill_subject,
    MIN(representatives_accept_date) as first_representatives_accept_date,
    MAX(representatives_finish_date) as last_representatives_finish_date,
    MIN(councilors_accept_date) as first_councilors_accept_date,
    MAX(councilors_finish_date) as last_councilors_finish_date
FROM `myproject-420013.low.bill_of_low`
GROUP BY bill_type,
    submit_diet_no,
    submit_bill_no