select month(date_on), ser_id, title, count(date_on), count(date_off)
from services join connected_services using (ser_id)
where year(date_on) = '$report_year'
group by month(date_on), ser_id, title;
