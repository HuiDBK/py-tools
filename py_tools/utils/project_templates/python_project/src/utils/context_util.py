import contextvars

# 请求唯一id
REQUEST_ID: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")

# 任务追踪唯一id
TRACE_ID: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default="")
