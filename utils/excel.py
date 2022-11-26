#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { Excel文件操作工具模块 }
# @Date: 2022/04/03 19:34
import pandas as pd


class ExcelUtil(object):
    """ Excel文件操作工具类 """

    def __init__(self, file_path):
        """
        :param file_path: 文件导出路径
        """
        self.file_path = file_path
        self._col_mapping = None
        self._sheet_name = 'sheet1'
        self._data_list = list()

    def style(self, col_mapping: dict = None, sheet_name: str = 'sheet1'):
        """
        设置 Excel表头样式和sheet名称
        col_mapping: 列字段映射
        sheet_name: excel表sheet名称
        :return:
        """
        self._col_mapping = col_mapping
        self._sheet_name = sheet_name
        return self

    def data_list(self, *data_list):
        """
        设置Excel表的数据集
        data_list:
        :return:
        """
        self._data_list = self._data_list.extend(*data_list)
        return self

    def _to_excel(self, data_list, excel_writer):
        """
        根据Excel样式和数据集生成excel文件
        :param data_list:
        :param excel_writer:
        :return:
        """
        col_mapping = list(self._col_mapping) if self._col_mapping else None
        df = pd.DataFrame(data_list, columns=col_mapping)
        if col_mapping:
            df.rename(columns=self._col_mapping, inplace=True)
        df.to_excel(excel_writer, sheet_name=self._sheet_name, index=False)

    def to_excel(self, data_list, col_mapping: dict = None, sheet_name: str = 'sheet1'):
        """
        data_list: 数据集 List[dict] or List[list]
        col_mapping: 列字段映射
        sheet_name: excel表sheet名称
        :return:
        """
        # 没有设置Excel样式时, 默认采用数据项的字段名当表头, sheet_name为sheet1
        if not self._col_mapping:
            self.style(col_mapping, sheet_name)
        with pd.ExcelWriter(self.file_path) as excel_writer:
            self._to_excel(data_list, excel_writer)

    def to_excels(self, data_list):
        """
        多列表转带不同sheet的excel文件
        data_list: 大数据集 list[(data_collect, col_mapping, sheet_name)]
            data_collect: 数据集,
            col_mapping: 列字段映射,
            sheet_name: excel表sheet名称
        :return:
        """
        # 没有设置Excel样式时, 默认采用数据项的字段名当表头, sheet_name为sheet1
        with pd.ExcelWriter(self.file_path) as excel_writer:
            for data_collect, col_mapping, sheet_name in data_list:
                self.style(col_mapping, sheet_name)
                self._to_excel(data_collect, excel_writer)

    # 功能一致, 看个人习惯, 喜欢使用类方法还是实例方法
    @classmethod
    def list_to_excel(
            cls,
            data_collects: list,
            file_path: str,
            col_mapping: dict = None,
            sheet_name: str = 'Sheet1'
    ):
        """
        列表转excel文件
        data_collect: 数据集 List[dict] or List[list]
        file_path: 文件路径 or buffer
        col_mapping: 列字段映射
        :return:
        """
        with pd.ExcelWriter(file_path) as writer:
            _col_mapping = list(col_mapping) if col_mapping else None
            df = pd.DataFrame(data=data_collects, columns=_col_mapping)
            if col_mapping:
                df.rename(columns=col_mapping, inplace=True)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    @classmethod
    def multi_list_to_excel(
            cls,
            data_collects: list,
            file_path: str,
    ):
        """
        多列表转带不同sheet的excel文件
        data_collects: 大数据集 list[(data_collect, col_mapping, sheet_name)]
            data_collect: 数据集,
            col_mapping: 列字段映射,
            sheet_name: excel表sheet名称
        file_name: 文件名字
        :return:
        """
        with pd.ExcelWriter(file_path) as writer:
            for data_collect, col_mapping, sheet_name in data_collects:
                df = pd.DataFrame(data=data_collect, columns=list(col_mapping))
                df.rename(columns=col_mapping, inplace=True)
                df.to_excel(writer, sheet_name=sheet_name, index=False)


def main():
    # 准备数据
    user_list = [
        dict(id=i, name=f'hui_{i}', age=f'{18 + i}', sex=1) for i in range(5)
    ]
    user_col_mapping = {
        'id': '用户id',
        'name': '用户名',
        'age': '年龄',
    }
    user_col_mapping2 = {
        'id': '用户id',
        'name': '用户名',
        'sex': '性别',
        'age': '年龄',
    }

    data_collects = [
        (user_list, user_col_mapping, 'demo_01'),
        (user_list, user_col_mapping2, 'demo_02'),
        (user_list, user_col_mapping, 'demo_03'),
    ]

    ExcelUtil(file_path='../tmp/test.xlsx').to_excel(user_list)

    ExcelUtil(file_path='../tmp/test.xlsx').style(
        col_mapping=user_col_mapping,
        sheet_name='test'
    ).to_excel(data_list=user_list)

    # 导出带多个sheet
    ExcelUtil(file_path='../tmp/many_demo.xlsx').to_excels(data_collects)

    # 以下为类方法, 同样的功能
    ExcelUtil.list_to_excel(
        user_list,
        file_path='../tmp/demo.xlsx',
        col_mapping=user_col_mapping,
        sheet_name='demo'
    )
    ExcelUtil.multi_list_to_excel(data_collects=data_collects, file_path='../tmp/many_demo.xlsx')


if __name__ == '__main__':
    main()
