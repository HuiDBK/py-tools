#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { Excel文件操作工具模块 }
# @Date: 2022/04/03 19:34
import pandas as pd
from typing import List, Union, Dict, IO


class ExcelUtil(object):
    """ Excel文件操作工具类 """

    @classmethod
    def list_to_excel(
            cls,
            path_or_buffer: Union[str, IO],
            data_list: list,
            col_mapping: dict = None,
            sheet_name: str = 'Sheet1',
            **kwargs
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
            df.to_excel(writer, sheet_name=sheet_name, index=False, **kwargs)

    @classmethod
    def multi_list_to_excel(
            cls,
            path_or_buffer: Union[str, IO],
            data_collects: List[tuple],
            **kwargs
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
                df.to_excel(writer, sheet_name=sheet_name, index=False, **kwargs)

    @classmethod
    def read_excel(
            cls,
            path_or_buffer: Union[str, IO],
            sheet_name: str = "Sheet1",
            col_mapping: dict = None,
            all_col: bool = True,
            header: int = 0,
            **kwargs
    ) -> List[dict]:
        """
        读取excel表格数据，根据col_mapping替换列名
        Args:
            path_or_buffer: 文件路径或者缓冲流
            sheet_name: 读书excel表的sheet名称
            col_mapping: 列字段映射
            all_col: True返回所有列信息，False则返回col_mapping对应的字段信息
            header: 默认0从第一行开启读取，用于指定从第几行开始读取

        Returns:
        """
        use_cols = None
        if not all_col:
            # 获取excel表指定列数据
            use_cols = list(col_mapping) if col_mapping else None

        df = pd.read_excel(path_or_buffer, sheet_name=sheet_name, usecols=use_cols, header=header, **kwargs)
        if col_mapping:
            df.rename(columns=col_mapping, inplace=True)

        return df.to_dict("records")

    @classmethod
    def merge_excel_files(
            cls,
            input_files: List[str],
            output_file: str,
            sheet_name_mapping: Dict[str, str] = None,
            **kwargs
    ):
        """
        合并多个Excel文件到一个文件中（每个文件对应一个工作表）
        如果Excel文件有多个作表，则默认取第一个工作表
        Args:
            input_files: 待合并的excel文件列表
            output_file: 输出文件路径
            sheet_name_mapping: 文件工作表映射，默认为文件名
                {"文件名1": "sheet1", "文件名2": "sheet2"}

        Returns:
        """
        sheet_name_mapping = sheet_name_mapping or {}
        with pd.ExcelWriter(output_file, **kwargs) as writer:
            for file in input_files:
                df = pd.read_excel(file)
                sheet_name = sheet_name_mapping.get(file, file)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
