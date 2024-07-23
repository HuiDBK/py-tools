#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 实用小函数模块 }
# @Date: 2023/09/10 00:07


def chunk_list(data_list: list, chunk_size: int) -> list:
    """
    等份切分列表
    Args:
        data_list: 数据列表
        chunk_size: 每份大小

    Returns: list
    """
    return [data_list[i : i + chunk_size] for i in range(0, len(data_list), chunk_size)]


def add_param_if_true(params, key, value, is_check_none=True):
    """
    值不为空则添加到参数字典中
    Args:
        params: 要加入元素的字典
        key: 要加入字典的key值
        value: 要加入字典的value值
        is_check_none: 是否只检查空值None, 默认True
            - True: 不允许None, 但允许 0、False、空串、空列表、空字典等是有意义的
            - False: 则不允许所有空值
    """
    if value or (is_check_none and value is not None):
        params[key] = value
