from py_tools.connections.db.mysql import DBManager
from src.dao.orm.table import UserTable


class UserManager(DBManager):
    orm_table = UserTable
