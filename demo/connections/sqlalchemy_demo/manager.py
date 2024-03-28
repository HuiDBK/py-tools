#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { sqlalchemy demo }
# @Date: 2023/09/04 14:22
from connections.sqlalchemy_demo.table import UserTable, UserFileTable
from py_tools.connections.db.mysql import DBManager


class UserManager(DBManager):
    orm_table = UserTable


class UserFileManager(DBManager):
    orm_table = UserFileTable
