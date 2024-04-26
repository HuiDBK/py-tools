from src.dao.orm.table import UserTable

from py_tools.connections.db.mysql import DBManager


class UserManager(DBManager):
    orm_table = UserTable
