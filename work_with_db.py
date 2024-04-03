from DBconn import DBContextManager, RedisCache
from sql_provider import SQLProvider

from functools import wraps
import datetime
import os


def select_dict(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            products = cursor.fetchall()
            if products:
                products_dict = []
                schema = [item[0].encode('Windows 1251').decode('utf-8') for item in cursor.description]
                for product in products:
                    products_dict.append(dict(zip(schema, product)))
                return products_dict
            else:
                return None


def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            param_list.append(arg)
        res = cursor.callproc(proc_name, param_list)
        return res


def fetch_from_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis'])  # connection to redis
    ttl = cache_config['ttl']

    def wrapper_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cached_value = cache_conn.get_value(cache_name)  # Извлекаем из кэша

            if cached_value:
                return cached_value
            response = f(*args, **kwargs)
            cache_conn.set_value(cache_name, response, ttl=ttl)
            return response

        return wrapper

    return wrapper_func


def clean_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis'])  # connection to redis
    cache_conn.del_value(cache_name)


def save_order_with_list(dbconfig: dict, user_id: int, current_basket: list, connected: list):
    with DBContextManager(dbconfig) as cursor:
        provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'blueprint_market\sql'))
        print(provider)
        if cursor is None:
            raise ValueError('curs doesnt exist')
        cur_date = datetime.datetime.now()
        print(connected, current_basket)
        for item in current_basket:
            if item in connected:
                _sql = provider.get('was_connected.sql', cl_id=user_id, ser_id=item)
                dt = select_dict(dbconfig, _sql)[0]['max(date_on)']
                if not dt:
                    return 0
                _sql = provider.get('insert_disconnect.sql', cl_id=user_id,
                                     dt_on=dt, ser_id=item, dt_off=cur_date)
                cursor.execute(_sql)
            else:
                _sql = provider.get('insert_connect.sql', cl_id=user_id,
                                     dt=cur_date, ser_id=item)
                cursor.execute(_sql)
        return 1
