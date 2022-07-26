from typing import List


class Query:
    def __init__(self, table: str):
        self.__base = ""
        self.__fields: List[str] = []
        self.__condition = ""
        self.__group_by = ""
        self.__order_by = ""
        self.__desc = ""
        self.__table = table

    def query_type(self):
        return self.__base.split(' ')[0]

    def select(self, fields: List[str] = None):
        if fields is None:
            fields = ['*']
        self.__base = f'select {",".join(fields)} from {self.__table}'
        self.__fields = fields
        return self

    def delete(self):
        self.__base = f'delete from {self.__table}'
        return self

    def update(self, sets: dict):
        set_string = ''
        for key in sets.keys():
            set_string += f'{key} = {sets[key]},'
        set_string = set_string[:-1]
        self.__base = f'update {self.__table} SET {set_string}'
        return self

    def where(self, condition: str):
        self.__condition = f'where {condition}'
        return self

    def group_by(self, fields: List[str]):
        self.__group_by = f'group by {",".join(fields)}'
        return self

    def order_by(self, field: str):
        self.__order_by = f'order by {field}'
        return self

    def desc(self):
        self.__desc = 'DESC'
        return self

    def build(self):
        return f"{self.__base} {self.__condition} {self.__group_by} {self.__order_by} {self.__desc}".rstrip() + ';'