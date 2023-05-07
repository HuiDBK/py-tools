import time

import pytest

from py_tools.decorators import retry, set_timeout
from py_tools.exceptions import MaxRetryException, MaxTimeoutException


class TestBaseDecorator:
    """通用装饰器测试"""

    @retry(max_count=3)
    def user_place_order_success(self):
        """用户下单成功模拟"""
        return {"code": 0, "msg": "ok"}

    @retry(max_count=3, interval=3)
    def user_place_order_fail(self):
        """用户下单失败重试模拟"""
        a = 1 / 0
        return {"code": 0, "msg": "ok"}

    def test_retry(self):
        """重试装饰器单测"""
        ret = self.user_place_order_success()
        assert ret["code"] == 0

        # 超过最大重试次数模拟
        with pytest.raises(MaxRetryException):
            self.user_place_order_fail()

    @set_timeout(3)
    def user_place_order(self):
        """用户下单超时模拟"""
        time.sleep(1)  # 模拟业务超时
        return {"code": 0, "msg": "ok"}

    @set_timeout(2)
    def user_place_order_timeout(self):
        """用户下单模拟"""
        time.sleep(3)  # 模拟业务超时
        return {"code": 0, "msg": "ok"}

    def test_timeout(self):
        """超时装饰器单测"""

        ret = self.user_place_order()
        assert ret.get("code") == 0

        # 超时
        with pytest.raises(MaxTimeoutException):
            self.user_place_order_timeout()
