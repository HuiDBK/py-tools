#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { sqlalchemy demo }
# @Date: 2023/09/04 14:22
import asyncio
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from py_tools.connections.db.mysql import SQLAlchemyManager, DBManager, BaseOrmTable, BaseOrmTableWithTS

db_client = SQLAlchemyManager(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123456",
    db_name="hui-demo",
)


class UserTable(BaseOrmTableWithTS):
    """用户表"""

    __tablename__ = "user"
    username: Mapped[str] = mapped_column(default="", comment="用户昵称")
    password: Mapped[str] = mapped_column(default="", comment="用户密码")
    phone: Mapped[str] = mapped_column(default="", comment="手机号")
    email: Mapped[str] = mapped_column(default="", comment="邮箱")
    avatar: Mapped[str] = mapped_column(default="", comment="头像")


class UserFileTable(BaseOrmTable):
    """用户文件表"""

    __tablename__ = "user_file"
    filename: Mapped[str] = mapped_column(default="", comment="文件名称")
    creator: Mapped[int] = mapped_column(default=0, comment="文件创建者")
    file_suffix: Mapped[str] = mapped_column(default="", comment="文件后缀")
    file_size: Mapped[int] = mapped_column(default=0, comment="文件大小")
    oss_key: Mapped[str] = mapped_column(default="", comment="oss key（minio）")
    is_del: Mapped[int] = mapped_column(default=0, comment="是否删除")
    deleted_at: Mapped[datetime] = mapped_column(nullable=True, comment="删除时间")


class UserManger(DBManager):
    table = UserTable


class UserFileManager(DBManager):
    orm_table = UserFileTable


async def mysql_demo():
    db_client.init_mysql_engine()
    DBManager.init_db_client(db_client)

    sql = """select * from user_basic"""
    ret = await UserManager().run_sql(sql=sql)

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

    ret = await UserFileManager().update(values={"filename": "hui"}, conds=[UserFileTable.id == 1])
    print("update ret", ret)

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

    total_count, data_list = await UserFileManager().list_page(
        cols=["filename", "oss_key", "file_size"], curr_page=2, page_size=10
    )
    print("total_count", total_count, f"data_list[{len(data_list)}]", data_list)

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
    print(ret)


async def main():
    await mysql_demo()


if __name__ == '__main__':
    asyncio.run(main())
