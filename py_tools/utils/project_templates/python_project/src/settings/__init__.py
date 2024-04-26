#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目配置包初始化 }
# @Date: 2023/09/07 16:38
from .base_setting import server_host, server_log_level, server_port
from .db_setting import (
    mysql_dbname, mysql_host, mysql_password, mysql_port, mysql_user,
    redis_db, redis_host, redis_password, redis_port
)
from .log_setting import console_log_level, logging_conf
