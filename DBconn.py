import json
from typing import Any, Optional, Dict

from redis import Redis, ConnectionError, DataError
from pymysql import connect
from pymysql import OperationalError


class DBContextManager:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            print(err.args)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type)
            print(exc_val.args)
        if self.cursor and self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True


class RedisCache:

    def __init__(self, config: dict):
        self.config = config
        self.conn = self._connect()

    def _connect(self) -> Redis:
        conn = Redis(**self.config)
        return conn

    def _update_connect_if_need(self) -> None:
        try:
            _ = self.conn.ping()
        except ConnectionError:
            self.conn = self._connect()

    def set_value(self, name: str, value: Dict, ttl: float = 0) -> bool:
        self._update_connect_if_need()
        try:
            value1 = json.dumps(value)
            self.conn.set(name=name, value=value1)# в качестве значения передаем словарь
            if ttl > 0:
                self.conn.expire(name, ttl)
            return True
        except DataError as e:
            print(f"err while setting key-value: {str(e)}")
            return False

    def get_value(self, name: str) -> Optional[Any]:
        self._update_connect_if_need()
        value = self.conn.get(name)
        if value:
            return json.loads(value)
        return None

    def del_value(self, name: str):
        self._update_connect_if_need()
        value = self.conn.get(name)
        if value:
            self.conn.delete(name)
            print(1)
