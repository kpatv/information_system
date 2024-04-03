select cl_id, name, birthday, passport, address, date_concl from client left join (select history.change_balance_date, cl_id from history where year(change_balance_date) = '$year'
and month(change_balance_date)='$month' )hist using (cl_id)
		where change_balance_date is NULL;
