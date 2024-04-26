#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 日志链路追踪工具模块 }
# @Date: 2023/10/30 15:51
import uuid

from src.utils import context_util


class TraceUtil(object):
    @staticmethod
    def set_req_id(req_id: str = None, title="req-id") -> str:
        """
        设置请求唯一ID
        Args:
            req_id: 请求ID 默认None取uuid
            title: 标题 默认req-id

        Returns:
            title:req_id
        """
        req_id = req_id or uuid.uuid4().hex
        req_id = f"{title}:{req_id}"

        context_util.REQUEST_ID.set(req_id)
        return req_id

    @staticmethod
    def set_trace_id(trace_id: str = None, title="trace-id") -> str:
        """
        设置追踪ID, 可用于一些脚本等场景进行链路追踪
        Args:
            trace_id: 追踪唯一ID 默认None取uuid
            title: 标题 默认 trace-id, 可以用于标识业务

        Returns:
            title:trace_id
        """
        trace_id = trace_id or uuid.uuid4().hex
        trace_id = f"{title}:{trace_id}"

        context_util.TRACE_ID.set(trace_id)
        return trace_id
