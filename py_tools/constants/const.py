#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: const.py
# @Desc: { 常量模块 }
# @Date: 2024/07/23 13:49
from pathlib import Path

# 默认的缓存key前缀
CACHE_KEY_PREFIX = "py-tools"

# 项目基准目录
BASE_DIR = Path(__file__).parent.parent.parent

# 案例目录
DEMO_DIR = BASE_DIR / "demo"

# 案例数据目录
DEMO_DATA = DEMO_DIR / "data"

# 项目源代码目录
PROJECT_DIR = BASE_DIR / "py_tools"

# 测试目录
TEST_DIR = BASE_DIR / "tests"
