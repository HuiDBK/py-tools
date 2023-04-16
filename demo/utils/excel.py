#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { excel操作案例 }
# @Date: 2023/04/17 0:31
from io import BytesIO

from utils import ExcelUtil


def list_to_excel_demo():
    user_list = [
        dict(id=1, name='hui', age=20),
        dict(id=2, name='wang', age=22),
        dict(id=3, name='zack', age=25),
    ]
    user_col_mapping = {
        'id': '用户id',
        'name': '用户名',
        'age': '年龄',
    }

    ExcelUtil.list_to_excel('user.xlsx', user_list, col_mapping=user_col_mapping)

    # 导出为excel文件字节流处理
    excel_bio = BytesIO()
    ExcelUtil.list_to_excel(
        excel_bio,
        data_list=user_list,
        col_mapping=user_col_mapping,
        sheet_name='buffer_demo'
    )
    excel_bytes = excel_bio.getvalue()
    print("excel_bytes type => ", type(excel_bytes))

    # 这里以重新写到文件里为例，字节流再业务中按需操作即可
    with open("user_byte.xlsx", mode="wb") as f:
        f.write(excel_bytes)


def multi_list_to_excel_demo():
    user_list = [
        {'id': 1, 'name': 'hui', 'age': 18},
        {'id': 2, 'name': 'wang', 'age': 19},
        {'id': 3, 'name': 'zack', 'age': 20}
    ]

    book_list = [
        {'id': 1, 'name': 'Python基础教程', 'author': 'hui', 'price': 30},
        {'id': 2, 'name': 'Java高级编程', 'author': 'wang', 'price': 50},
        {'id': 3, 'name': '机器学习实战', 'author': 'zack', 'price': 70},
    ]

    user_col_mapping = {'id': '编号', 'name': '姓名', 'age': '年龄'}
    book_col_mapping = {'id': '编号', 'name': '书名', 'author': '作者', 'price': '价格'}

    data_collects = [
        (user_list, user_col_mapping, '用户信息'),
        (book_list, book_col_mapping, '图书信息')
    ]

    ExcelUtil.multi_list_to_excel('multi_sheet_data.xlsx', data_collects)


def read_excel_demo():
    data = [
        {"id": 1, "name": "hui", "age": 30},
        {"id": 2, "name": "zack", "age": 25},
        {"id": 3, "name": "wang", "age": 40},
    ]

    # 将数据写入Excel文件
    ExcelUtil.list_to_excel("read_demo.xlsx", data, col_mapping={"id": "用户ID", "name": "姓名", "age": "年龄"})

    # 读取Excel文件
    result = ExcelUtil.read_excel("read_demo.xlsx", col_mapping={"用户ID": "id", "姓名": "name"}, all_col=False)

    print(result)


def merge_excel_files_demo():
    # 合并多个Excel文件
    ExcelUtil.merge_excel_files(
        input_files=["user.xlsx", "multi_sheet_data.xlsx"],
        output_file="merged_data.xlsx",
        sheet_name_mapping={
            "user.xlsx": "user",
            "multi_sheet_data.xlsx": "multi_sheet_data"
        }
    )


def main():
    list_to_excel_demo()

    multi_list_to_excel_demo()

    read_excel_demo()

    merge_excel_files_demo()


if __name__ == '__main__':
    main()
