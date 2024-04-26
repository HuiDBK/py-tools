import logging
import os
import sys

# 项目基准路径
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 项目日志目录
logging_dir = os.path.join(base_dir, "logs/")

# 项目运行时所有的日志文件
server_log_file = os.path.join(logging_dir, "server.log")

# 错误时的日志文件
error_log_file = os.path.join(logging_dir, "error.log")

# 项目服务综合日志滚动配置（每天 0 点新创建一个 log 文件）
# 错误日志 超过10 MB就自动新建文件扩充
server_logging_rotation = "00:00"
error_logging_rotation = "10 MB"

# 服务综合日志文件最长保留 7 天，错误日志 30 天
server_logging_retention = "7 days"
error_logging_retention = "30 days"

# 项目日志配置
console_log_level = logging.DEBUG
log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {trace_msg} | {name}:{function}:{line} - {message}"

logging_conf = {
    "console_handler": {
        "sink": sys.stdout,
        "level": console_log_level,
        # "format": log_format, # 开启控制台也会输出 trace_msg 信息但日志没有颜色了
    },
    "server_handler": {
        "sink": server_log_file,
        "level": "INFO",
        "rotation": server_logging_rotation,
        "retention": server_logging_retention,
        "enqueue": True,
        "backtrace": False,
        "diagnose": False,
        "format": log_format,
    },
    "error_handler": {
        "sink": error_log_file,
        "level": "ERROR",
        "rotation": error_logging_rotation,
        "retention": error_logging_retention,
        "enqueue": True,
        "backtrace": True,
        "diagnose": True,
        "format": log_format,
    },
}
