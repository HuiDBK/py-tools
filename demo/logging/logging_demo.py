#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: logging_demo.py
# @Desc: { 日志使用案例 }
# @Date: 2024/08/12 14:53
import logging

from py_tools.constants import BASE_DIR
from py_tools.logging import logger, setup_logging
from py_tools.logging.default_logging_conf import default_logging_conf


def main():
    setup_logging(log_dir=BASE_DIR / "logs")
    logger.info("use log dir")
    logger.error("test error")

    log_conf = default_logging_conf.get("server_handler")
    log_conf["sink"] = BASE_DIR / "logs/server.log"
    setup_logging(log_conf=log_conf, console_log_level=logging.WARN)

    logger.info("use log conf")
    logger.error("test error")


if __name__ == "__main__":
    main()
