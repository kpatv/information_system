import os
from string import Template


class SQLProvider:
    def __init__(self, file_path: str):
        self._scripts = {}
        for file in os.listdir(file_path):
            # sql = open(f"{file_path}/{file}").read()
            sql = open(f"{file_path}/{file}", encoding="utf-8").read()
            self._scripts[file] = Template(
                sql)  # открыли файл path, путь к директории с sql-запросами, для каждого файла читаем, открываем, считываем запрос, занесли в словарь, где ключ - имя файла, а значение - запрос

    def get(self, name, **kwargs):
        sql = self._scripts[name].substitute(**kwargs)
        return sql
