select
    report_year as 'Year',
    report_month as 'Month',
    cl_id as 'client ID',
    name as 'Name',
    change_balance_sum as 'The amount of changes'
from report_change_balance_cl
where report_year = "$year_" and report_month = "$month_"