#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: tree.py
# @Desc: { 树形结构相关工具函数 }
# @Date: 2024/04/24 11:54
from typing import List


def list_to_tree_dfs(
    data_list: List[dict],
    root_pid: int = 0,
    pid_field: str = "pid",
    sub_field: str = "children",
    relate_field: str = "id",
    level: int = 0,
    need_level: bool = False,
):
    """
    递归构造树形列表(深度优先)

    Args:
        data_list: 待转换为树形结构的字典列表
        root_pid: 根节点的父节点标识符，默认为 0
        pid_field: 字典中表示父节点标识符的字段名，默认为 "pid"
        sub_field: 子节点列表的字段名，默认为 "children"
        relate_field: 父子级关联字段，默认为 "id"，例如 pid 与 id 关联
        level: 当前节点的层级，默认为 0
        need_level: 是否需要记录节点的层级，默认为 False

    Returns: 树形列表
    """
    children = []
    level = level + 1  # 记录层级
    for node in data_list:
        if node[pid_field] == root_pid:
            # 递归调用
            node[sub_field] = list_to_tree_dfs(
                data_list, node[relate_field], pid_field, sub_field, relate_field, level, need_level
            )
            if need_level:
                node["level"] = level
            children.append(node)
    return children


def list_to_tree_bfs(
    data_list: List[dict],
    root_pid: int = 0,
    pid_field: str = "pid",
    sub_field: str = "children",
    relate_field: str = "id",
    level: int = 0,
    need_level: bool = False,
):
    """
    构造树形列表(广度优先)

    Args:
        data_list: 待转换为树形结构的字典列表
        root_pid: 根节点的父节点标识符，默认为 0
        pid_field: 字典中表示父节点标识符的字段名，默认为 "pid"
        sub_field: 子节点列表的字段名，默认为 "children"
        relate_field: 父子级关联字段，默认为 "id"，例如 pid 与 id 关联
        level: 当前节点的层级，默认为 0
        need_level: 是否需要记录节点的层级，默认为 False

    Returns: 树形列表
    """
    queue = [(node, level + 1) for node in data_list if node[pid_field] == root_pid]

    tree_list = []
    while queue:
        node, node_level = queue.pop(0)

        # 所有的子节点加入队列
        children = []
        for child in data_list:
            if child[pid_field] == node[relate_field]:
                queue.append((child, node_level + 1))
                children.append(child)

        node[sub_field] = children
        if need_level:
            node["level"] = node_level

        if node[pid_field] == root_pid:
            # 只有顶级节点才添加
            tree_list.append(node)

    return tree_list


def tree_to_list_dfs(tree_list, sub_field="children", result_list=None, level=0, need_level=False):
    """
    将树形结构列表扁平化成一层列表（深度优先）

    Args:
        tree_list: 树形结构列表
        sub_field: 子节点列表的字段名，默认为 "children"
        result_list: 保存结果的列表
        level: 当前节点的层级，默认为 0
        need_level: 是否需要记录节点的层级，默认为 False

    Returns: 扁平化后的一层列表
    """
    result_list = result_list or []
    level = level + 1

    for node in tree_list:
        if need_level:
            node["level"] = level
        result_list.append(node)
        sub_list = node.pop(sub_field, None)
        if sub_list:
            tree_to_list_dfs(sub_list, sub_field, result_list, level, need_level)

    return result_list


def tree_to_list_bfs(tree_list, sub_field="children", level=0, need_level=False):
    """
    将树形结构列表扁平化成一层列表（广度优先）

    Args:
        tree_list: 树形结构列表
        sub_field: 子节点列表的字段名，默认为 "children"
        level: 当前节点的层级，默认为 0
        need_level: 是否需要记录节点的层级，默认为 False

    Returns: 扁平化后的一层列表
    """
    result_list = []
    queue = [(node, level + 1) for node in tree_list]

    while queue:
        node, cur_level = queue.pop(0)  # 取出队首节点
        children = node.pop(sub_field, [])
        if need_level:
            node["level"] = cur_level
        result_list.append(node)
        queue.extend((child, cur_level + 1) for child in children)

    return result_list
