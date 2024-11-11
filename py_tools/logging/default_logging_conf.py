#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: default_logging_conf.py
# @Desc: { 默认日志配置 }
# @Date: 2024/08/12 10:57
import logging
import sys

from py_tools.constants import BASE_DIR

# 项目日志目录
logging_dir = BASE_DIR / "logs"

# 项目运行时所有的日志文件
server_log_file = logging_dir / "server.log"

# 错误时的日志文件
error_log_file = logging_dir / "error.log"

# 项目服务综合日志滚动配置（每天 0 点新创建一个 log 文件）
# 错误日志 超过10 MB就自动新建文件扩充
server_logging_rotation = "00:00"
error_logging_rotation = "10 MB"

# 服务综合日志文件最长保留 7 天，错误日志 30 天
server_logging_retention = "7 days"
error_logging_retention = "30 days"

# 项目日志配置
console_log_level = logging.DEBUG
trace_msg_log_format = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {trace_msg} | {name}:{function}:{line} - {message}"
)
default_log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}"
console_log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level:<8}</level> | "
    "<level>{name}:{function}:{line} - {message}</level>"
)

default_logging_conf = {
    "console_handler": {
        "sink": sys.stdout,
        "level": console_log_level,
    },
    "server_handler": {
        "sink": server_log_file,
        "level": "INFO",
        "rotation": server_logging_rotation,
        "retention": server_logging_retention,
        "enqueue": True,
        "backtrace": False,
        "diagnose": False,
    },
    "error_handler": {
        "sink": error_log_file,
        "level": "ERROR",
        "rotation": error_logging_rotation,
        "retention": error_logging_retention,
        "enqueue": True,
        "backtrace": True,
        "diagnose": True,
    },
}
