#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { Excel文件操作工具模块 }
# @Date: 2022/04/03 19:34
import os
from typing import IO, List, Union

import numpy as np
import pandas
from pydantic import BaseModel, Field


class ColumnMapping(BaseModel):
    """列名映射"""

    column_name: str = Field(description="列名")
    column_alias: str = Field(description="列名别名")


class SheetMapping(BaseModel):
    """sheet映射"""

    file_name: str = Field(description="文件名")
    sheet_name: str = Field(description="sheet名")


class DataCollect(BaseModel):
    """多sheet的数据集合"""

    data_list: List[dict] = Field(description="数据列表")
    col_mappings: List[ColumnMapping] = Field(description="列名映射列表")
    sheet_name: str = Field(description="sheet名称")


class ExcelUtil(object):
    """Excel文件操作工具类"""

    DEFAULT_SHEET_NAME = "Sheet1"

    @classmethod
    def _to_excel(
        cls, data_list: List[dict], col_mappings: List[ColumnMapping], sheet_name: str, writer: pandas.ExcelWriter, **kwargs
    ):
        """
        将列表数据写入excel文件
        Args:
            path_or_buffer: 文件路径或者字节缓冲流
            data_list: 数据集 List[dict]
            col_mappings: 表头列字段映射
            sheet_name: sheet名称 默认 Sheet1
            writer: ExcelWriter
        """
        col_dict = {cm.column_name: cm.column_alias for cm in col_mappings} if col_mappings else None
        df = pandas.DataFrame(data=data_list)
        if col_dict:
            df.rename(columns=col_dict, inplace=True)
        df.to_excel(writer, sheet_name=sheet_name, index=False, **kwargs)

    @classmethod
    def list_to_excel(
        cls,
        path_or_buffer: Union[str, IO],
        data_list: List[dict],
        col_mappings: List[ColumnMapping] = None,
        sheet_name: str = None,
        **kwargs
    ):
        """
        列表转 excel文件
        Args:
            path_or_buffer: 文件路径或者字节缓冲流
            data_list: 数据集 List[dict]
            col_mappings: 表头列字段映射
            sheet_name: sheet名称 默认 Sheet1
            writer: ExcelWriter

        Examples:
            data_list = [{"id": 1, "name": "hui", "age": 18}]
            user_col_mapping = [
                    ColumnMapping('id', '用户id'),
                    ColumnMapping('name', '用户名'),
                    ColumnMapping('age', '年龄'),
            ]
            ExcelUtil.list_to_excel('path_to_file', data_list, user_col_mapping)

        Returns:
        """
        sheet_name = sheet_name or cls.DEFAULT_SHEET_NAME
        with pandas.ExcelWriter(path_or_buffer) as writer:
            cls._to_excel(data_list, col_mappings, sheet_name, writer, **kwargs)

    @classmethod
    def multi_list_to_excel(cls, path_or_buffer: Union[str, IO], data_collects: List[DataCollect], **kwargs):
        """
        多列表转带不同 sheet的excel文件
        Args:
            path_or_buffer: 文件路径或者字节缓冲流
            data_collects: 数据集列表

        Returns:
        """
        with pandas.ExcelWriter(path_or_buffer) as writer:
            for data_collect in data_collects:
                cls._to_excel(
                    data_list=data_collect.data_list,
                    col_mappings=data_collect.col_mappings,
                    sheet_name=data_collect.sheet_name,
                    writer=writer,
                    **kwargs,
                )

    @classmethod
    def read_excel(
        cls,
        path_or_buffer: Union[str, IO],
        sheet_name: str = None,
        col_mappings: List[ColumnMapping] = None,
        all_col: bool = True,
        header: int = 0,
        nan_replace=None,
        **kwargs
    ) -> List[dict]:
        """
        读取excel表格数据，根据col_mapping替换列名
        Args:
            path_or_buffer: 文件路径或者缓冲流
            sheet_name: 读书excel表的sheet名称
            col_mappings: 列字段映射
            all_col: True返回所有列信息，False则返回col_mapping对应的字段信息
            header: 默认0从第一行开启读取，用于指定从第几行开始读取
            nan_replace: nan值替换，默认替换成None

        Returns:
        """
        sheet_name = sheet_name or cls.DEFAULT_SHEET_NAME
        col_dict = {cm.column_name: cm.column_alias for cm in col_mappings} if col_mappings else None
        use_cols = None
        if not all_col:
            # 获取excel表指定列数据
            use_cols = list(col_dict) if col_dict else None

        df = pandas.read_excel(path_or_buffer, sheet_name=sheet_name, usecols=use_cols, header=header, **kwargs)
        df.replace(np.NAN, nan_replace)
        if col_dict:
            df.rename(columns=col_dict, inplace=True)

        return df.to_dict("records")

    @classmethod
    def merge_excel_files(cls, input_files: List[str], output_file: str, sheet_mappings: List[SheetMapping] = None, **kwargs):
        """
        合并多个Excel文件到一个文件中（每个文件对应一个工作表）
        如果Excel文件有多个作表，则默认取第一个工作表
        Args:
            input_files: 待合并的excel文件列表
            output_file: 输出文件路径
            sheet_mappings: 文件工作表映射，默认为文件名

        Returns:
        """
        sheet_mappings = sheet_mappings or []
        sheet_dict = {sheet_mapping.file_name: sheet_mapping.sheet_name for sheet_mapping in sheet_mappings}
        with pandas.ExcelWriter(output_file, engine_kwargs=kwargs) as writer:
            for file in input_files:
                df = pandas.read_excel(file)
                file_name = os.path.basename(file)
                sheet_name = sheet_dict.get(file_name, file_name)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
