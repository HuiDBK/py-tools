#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { sqlalchemy demo }
# @Date: 2023/09/04 14:22
import asyncio

from py_tools.connections.db.mysql import SQLAlchemyManager, DBManager

db_client = SQLAlchemyManager(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="hui2023quan",
    db_name="task_flow",
)


async def mysql_demo():
    db_client.init_mysql_engine()
    db_manager = DBManager(db_client=db_client)
    sql = """select * from user_basic"""
    ret = await db_manager.run_sql(sql=sql)
    print(ret.all())


async def main():
    await mysql_demo()


if __name__ == '__main__':
    asyncio.run(main())