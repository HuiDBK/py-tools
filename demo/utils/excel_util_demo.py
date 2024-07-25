#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { excel操作案例 }
# @Date: 2023/04/17 0:31
from io import BytesIO

from py_tools.constants import DEMO_DATA
from py_tools.logging import logger
from py_tools.utils import ExcelUtil
from py_tools.utils.excel_util import ColumnMapping, DataCollect, SheetMapping


def list_to_excel_demo():
    user_list = [
        dict(id=1, name="hui", age=20),
        dict(id=2, name="wang", age=22),
        dict(id=3, name="zack", age=25),
    ]
    user_col_mappings = [
        ColumnMapping(column_name="id", column_alias="用户id"),
        ColumnMapping(column_name="name", column_alias="用户名"),
        ColumnMapping(column_name="age", column_alias="年龄"),
    ]

    file_path = DEMO_DATA / "user.xlsx"
    ExcelUtil.list_to_excel(file_path, user_list, col_mappings=user_col_mappings)

    # 导出为excel文件字节流处理
    excel_bio = BytesIO()
    ExcelUtil.list_to_excel(excel_bio, data_list=user_list, col_mappings=user_col_mappings, sheet_name="buffer_demo")
    excel_bytes = excel_bio.getvalue()
    logger.debug(f"excel_bytes type => {type(excel_bytes)}")

    # 这里以重新写到文件里为例，字节流再业务中按需操作即可
    with open(f"{DEMO_DATA}/user_byte.xlsx", mode="wb") as f:
        f.write(excel_bytes)


def multi_list_to_excel_demo():
    user_list = [
        {"id": 1, "name": "hui", "age": 18},
        {"id": 2, "name": "wang", "age": 19},
        {"id": 3, "name": "zack", "age": 20},
    ]

    book_list = [
        {"id": 1, "name": "Python基础教程", "author": "hui", "price": 30},
        {"id": 2, "name": "Java高级编程", "author": "wang", "price": 50},
        {"id": 3, "name": "机器学习实战", "author": "zack", "price": 70},
    ]

    user_col_mappings = [
        ColumnMapping(column_name="id", column_alias="编号"),
        ColumnMapping(column_name="name", column_alias="姓名"),
        ColumnMapping(column_name="age", column_alias="年龄"),
    ]
    book_col_mappings = [
        ColumnMapping(column_name="id", column_alias="编号"),
        ColumnMapping(column_name="name", column_alias="书名"),
        ColumnMapping(column_name="author", column_alias="作者"),
        ColumnMapping(column_name="price", column_alias="价格"),
    ]

    data_collects = [
        DataCollect(data_list=user_list, col_mappings=user_col_mappings, sheet_name="用户信息"),
        DataCollect(data_list=book_list, col_mappings=book_col_mappings, sheet_name="图书信息"),
    ]

    ExcelUtil.multi_list_to_excel(f"{DEMO_DATA}/multi_sheet_data.xlsx", data_collects)


def read_excel_demo():
    data = [
        {"id": 1, "name": "hui", "age": 30},
        {"id": 2, "name": "zack", "age": 25},
        {"id": 3, "name": "", "age": 40},
    ]

    user_col_mappings = [
        ColumnMapping(column_name="id", column_alias="用户id"),
        ColumnMapping(column_name="name", column_alias="用户名"),
        ColumnMapping(column_name="age", column_alias="年龄"),
    ]

    user_id_and_name_mappings = [
        ColumnMapping(column_name="用户id", column_alias="id"),
        ColumnMapping(column_name="用户名", column_alias="name"),
    ]

    # 将数据写入Excel文件
    file_path = DEMO_DATA / "read_demo.xlsx"
    ExcelUtil.list_to_excel(file_path, data, col_mappings=user_col_mappings)

    # 读取Excel文件
    result = ExcelUtil.read_excel(file_path, col_mappings=user_id_and_name_mappings, all_col=False, nan_replace="")

    logger.debug(f"read_excel {result}")


def merge_excel_files_demo():
    # 合并多个Excel文件
    ExcelUtil.merge_excel_files(
        input_files=[f"{DEMO_DATA}/user.xlsx", f"{DEMO_DATA}/multi_sheet_data.xlsx"],
        output_file=f"{DEMO_DATA}/merged_data.xlsx",
        sheet_mappings=[
            SheetMapping(file_name="user.xlsx", sheet_name="user"),
            SheetMapping(file_name="multi_sheet_data.xlsx", sheet_name="multi_sheet_data"),
        ],
    )


def main():
    list_to_excel_demo()

    multi_list_to_excel_demo()

    read_excel_demo()

    merge_excel_files_demo()


if __name__ == "__main__":
    main()
