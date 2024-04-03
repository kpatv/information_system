select ser_id from (select ser_id, max(date_on), max(date_off) from connected_services where cl_id = "$cl_id" group by ser_id)m
    where `max(date_on)` > `max(date_off)` or `max(date_off)` is null