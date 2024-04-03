select cl_id, name, sum(balance_new-balance_prev)
from client join history using (cl_id)
where year(change_balance_date)='$report_year' and month(change_balance_date)='$report_month'
and cl_id between '$x1' and '$x2'
group by cl_id, name;
