#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: base.py
# @Desc: { 日志配置相关函数 }
# @Date: 2024/08/12 11:12
import logging
from pathlib import Path
from typing import Type, Union

from py_tools.logging import logger
from py_tools.logging.default_logging_conf import (
    default_logging_conf,
    server_logging_retention,
    server_logging_rotation,
)
from py_tools.utils.func_util import add_param_if_true


def setup_logging(
    log_dir: Union[str, Path] = None,
    *,
    log_conf: dict = None,
    sink: Union[str, Path] = None,
    log_level: Union[str, int] = None,
    console_log_level: Union[str, int] = logging.DEBUG,
    log_format: str = None,
    log_filter: Type[callable] = None,
    log_rotation: str = server_logging_rotation,
    log_retention: str = server_logging_retention,
    **kwargs,
):
    """
    配置项目日志信息
    Args:
        log_dir (Union[str, Path]): 日志存储的目录路径。
        log_conf (dict): 项目的详细日志配置字典，可覆盖其他参数的设置。
        sink (Union[str, Path]): 日志文件sink
        log_level (Union[str, int]): 全局的日志级别，如 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' 或对应的整数级别。
        console_log_level (Union[str, int]): 控制台输出的日志级别，默认为 logging.DEBUG。
        log_format (str): 日志的格式字符串。
        log_filter (object): 用于过滤日志的可调用对象。
        log_rotation (str): 日志的轮转策略，例如按时间或大小轮转， 默认每天 0 点新创建一个 log 文件。
        log_retention (str): 日志的保留策略，指定保留的时间或数量，默认最长保留 7 天。
        **kwargs: 其他未明确指定的额外参数，用于未来的扩展或备用。

    Returns:
        None
    """
    logger.remove()
    logging_conf = {**default_logging_conf}
    logging_conf["console_handler"]["level"] = console_log_level

    log_conf = log_conf or {}
    log_conf.update(**kwargs)

    conf_mappings = {
        "sink": sink,
        "level": log_level,
        "format": log_format,
        "rotation": log_rotation,
        "retention": log_retention,
    }
    for key, val in conf_mappings.items():
        add_param_if_true(log_conf, key, val)

    if log_dir:
        log_dir = Path(log_dir)
        server_log_file = log_dir / "server.log"
        error_log_file = log_dir / "error.log"
        log_conf["sink"] = log_conf.get("sink") or server_log_file
        logging_conf["error_handler"]["sink"] = error_log_file
    else:
        if not log_conf.get("sink"):
            raise ValueError("log_conf must have `sink` key")

        sink_file = log_conf.get("sink")
        sink_file = Path(sink_file)
        error_log_file = sink_file.parent / "error.log"
        logging_conf["error_handler"]["sink"] = error_log_file

    add_param_if_true(logging_conf, "server_handler", log_conf)
    for log_handler, _log_conf in logging_conf.items():
        _log_conf["filter"] = log_filter
        logger.add(**_log_conf)

    logger.info("setup logging success")
