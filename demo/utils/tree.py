#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: tree.py
# @Desc: { 模块描述 }
# @Date: 2024/04/24 11:55
import copy
from pprint import pprint

from py_tools.utils.tree import list_to_tree_dfs, list_to_tree_bfs, tree_to_list_dfs, tree_to_list_bfs

depart_list = [
    {"id": 1, "name": "a1", "pid": 0},
    {"id": 2, "name": "a1_2", "pid": 1},
    {"id": 3, "name": "a1_3", "pid": 1},
    {"id": 4, "name": "a1_4", "pid": 1},
    {"id": 5, "name": "a2_1", "pid": 2},
    {"id": 6, "name": "a2_2", "pid": 2},
    {"id": 7, "name": "a3", "pid": 0},
    {"id": 8, "name": "a3_1", "pid": 7},
    {"id": 9, "name": "a3_2", "pid": 7},
    {"id": 10, "name": "a4", "pid": 0},
]


def main():
    depart_tree_list = list_to_tree_dfs(copy.deepcopy(depart_list), root_pid=0, sub_field="subs", need_level=False)
    depart_tree_list = list_to_tree_bfs(copy.deepcopy(depart_list), root_pid=0, sub_field="subs", need_level=True)

    print("原来列表")
    pprint(depart_list)

    print("列表 bfs=> 树形列表")
    pprint(depart_tree_list)

    print("树形列表 dfs=> 列表")
    pprint(tree_to_list_dfs(copy.deepcopy(depart_tree_list), sub_field="subs", need_level=True))

    print("树形列表 bfs=> 列表")
    pprint(tree_to_list_bfs(copy.deepcopy(depart_tree_list), sub_field="subs", need_level=True))

    print("原来树形列表")
    pprint(depart_tree_list)


if __name__ == '__main__':
    main()
