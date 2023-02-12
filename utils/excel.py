#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { Excel文件操作工具模块 }
# @Date: 2022/04/03 19:34
import pandas as pd
from typing import List, Union


class ExcelUtils(object):
    """ Excel文件操作工具类 """

    @classmethod
    def list_to_excel(
            cls,
            path_or_buffer,
            data_list: list,
            col_mapping: dict = None,
            sheet_name: str = 'Sheet1'
    ):
        """
        列表转 excel文件
        Args:
            path_or_buffer: 文件路径或者缓冲流
            data_list: 数据集 List[dict]
            col_mapping: 表头列字段映射
            sheet_name: sheet名称

        Returns:
        """
        with pd.ExcelWriter(path_or_buffer) as writer:
            _col_mapping = list(col_mapping) if col_mapping else None
            df = pd.DataFrame(data=data_list, columns=_col_mapping)
            if col_mapping:
                df.rename(columns=col_mapping, inplace=True)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    @classmethod
    def multi_list_to_excel(
            cls,
            path_or_buffer,
            data_collects: List[tuple],
    ):
        """
        多列表转带不同 sheet的excel文件
        Args:
            path_or_buffer: 文件路径或者缓冲流
            data_collects: 大数据集 list[(data_collect, col_mapping, sheet_name)]
                data_collect: 数据集,
                col_mapping: 列字段映射,
                sheet_name: excel表sheet名称

        Returns:
        """
        with pd.ExcelWriter(path_or_buffer) as writer:
            for data_collect, col_mapping, sheet_name in data_collects:
                df = pd.DataFrame(data=data_collect, columns=list(col_mapping))
                df.rename(columns=col_mapping, inplace=True)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    @classmethod
    def read_excel(
            cls,
            path_or_buffer,
            sheet_name: str = "Sheet1",
            col_mapping: dict = None,
            all_col: bool = True
    ) -> Union[dict, List[dict]]:
        """
        读取excel表格数据，根据col_mapping替换列名
        Args:
            path_or_buffer: 文件路径或者缓冲流
            sheet_name: 读书excel表的sheet名称
            col_mapping: 列字段映射
            all_col: True返回所有列信息，False则返回col_mapping对应的字段信息

        Returns:
        """
        use_cols = None
        if not all_col:
            # 获取excel表指定列数据
            use_cols = list(col_mapping) if col_mapping else None

        df = pd.read_excel(path_or_buffer, sheet_name=sheet_name, usecols=use_cols)
        if col_mapping:
            df.rename(columns=col_mapping, inplace=True)

        return df.to_dict("records")
