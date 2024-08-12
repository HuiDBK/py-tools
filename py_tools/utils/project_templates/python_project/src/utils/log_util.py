from src.utils import context_util


class LogUtil:
    @staticmethod
    def logger_filter(record):
        """日志过滤器补充request_id或trace_id"""
        req_id = context_util.REQUEST_ID.get()
        trace_id = context_util.TRACE_ID.get()

        trace_msg = f"{req_id} | {trace_id}"
        record["trace_msg"] = trace_msg
        return record
