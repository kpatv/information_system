select cl_id, name, birthday, passport, address, date_concl from client
where TIMESTAMPDIFF(YEAR, birthday, CURDATE()) <= '$client_age'
