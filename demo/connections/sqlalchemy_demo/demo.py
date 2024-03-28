#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { sqlalchemy demo }
# @Date: 2023/09/04 14:22
import asyncio
import uuid
from typing import List

from sqlalchemy import func

from connections.sqlalchemy_demo.manager import UserManager, UserFileManager
from connections.sqlalchemy_demo.table import UserFileTable
from py_tools.connections.db.mysql import SQLAlchemyManager, DBManager

db_client = SQLAlchemyManager(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123456",
    db_name="hui-demo",
)


async def create_and_transaction_demo():
    async with UserFileManager.transaction() as session:
        await UserFileManager().bulk_insert(
            add_rows=[{"filename": "aaa", "oss_key": uuid.uuid4().hex}], session=session
        )
        user_file_obj = UserFileTable(filename="eee", oss_key=uuid.uuid4().hex)
        file_id = await UserFileManager().add(table_obj=user_file_obj, session=session)
        print("file_id", file_id)

        ret: UserFileTable = await UserFileManager().query_by_id(2, session=session)
        print("query_by_id", ret)

        # a = 1 / 0

        ret = await UserFileManager().query_one(
            cols=[UserFileTable.filename, UserFileTable.oss_key],
            conds=[UserFileTable.filename == "ccc"],
            session=session
        )
        print("ret", ret)


async def query_demo():
    ret = await UserFileManager().query_one(conds=[UserFileTable.filename == "ccc"])
    print("ret", ret)

    file_count = await UserFileManager().query_one(cols=[func.count()], flat=True)
    print("str col one ret", file_count)

    filename = await UserFileManager().query_one(
        cols=[UserFileTable.filename],
        conds=[UserFileTable.id == 2],
        flat=True
    )
    print("filename", filename)

    ret = await UserFileManager().query_all(cols=[UserFileTable.filename, UserFileTable.oss_key])
    print("ret", ret)

    ret = await UserFileManager().query_all(cols=["filename", "oss_key"])
    print("str col ret", ret)

    ret: List[UserFileTable] = await UserFileManager().query_all()
    print("ret", ret)

    ret = await UserFileManager().query_all(cols=[UserFileTable.id], flat=True)
    print("ret", ret)


async def delete_demo():
    file_count = await UserFileManager().query_one(cols=[func.count()], flat=True)
    print("file_count", file_count)

    ret = await UserFileManager().delete_by_id(file_count)
    print("delete_by_id ret", ret)

    ret = await UserFileManager().bulk_delete_by_ids(pk_ids=[4, 7, 9])
    print("bulk_delete_by_ids ret", ret)

    ret = await UserFileManager().delete(conds=[UserFileTable.id == 9])
    print("delete ret", ret)

    ret = await UserFileManager().delete(conds=[UserFileTable.id == 1], logic_del=True)
    print("logic_del ret", ret)

    ret = await UserFileManager().delete(
        conds=[UserFileTable.id == 1], logic_del=True, logic_field="is_del", logic_del_set_value=1
    )
    print("logic_del set logic_field ret", ret)


async def update_demo():
    ret = await UserFileManager().update(values={"filename": "hui"}, conds=[UserFileTable.id == 1])
    print("update ret", ret)


async def list_page_demo():
    """分页查询demo"""
    total_count, data_list = await UserFileManager().list_page(
        cols=["filename", "oss_key", "file_size"], curr_page=2, page_size=10
    )
    print("total_count", total_count, f"data_list[{len(data_list)}]", data_list)


async def run_raw_sql_demo():
    """运行原生sql demo"""
    count_sql = "select count(*) as total_count from user_file"
    count_ret = await UserFileManager().run_sql(count_sql, query_one=True)
    print("count_ret", count_ret)

    data_sql = "select * from user_file where id > :id_val and file_size >= :file_size_val"
    params = {"id_val": 20, "file_size_val": 0}
    data_ret = await UserFileManager().run_sql(data_sql, params)
    print("dict data_ret", data_ret)

    data_sql = "select * from user_file where id > :id_val"
    data_ret = await UserFileManager().run_sql(sql=data_sql, params={"id_val": 4})
    print("dict data_ret", data_ret)


async def curd_demo():
    db_client.init_mysql_engine()
    DBManager.init_db_client(db_client)


async def main():
    await curd_demo()


if __name__ == '__main__':
    asyncio.run(main())
