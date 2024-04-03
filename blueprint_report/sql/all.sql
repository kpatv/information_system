select
    report_year as 'Year',
    report_month as 'Month',
    ser_id as 'Service ID',
    title as 'Title',
    count_ser as 'Count of connections'
from report_count_on_serv
where report_year = "$year_" and report_month = "$month_"