#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 时间工具类模块 }
# @Date: 2022/11/26 16:08

import time
from datetime import datetime, timedelta

from enums.time import TimeFormatEnum


class TimeUtils(object):

    def __init__(self, datetime_obj: datetime = None, format_str: str = TimeFormatEnum.DateTime.value):
        """
        时间工具类初始化
        Args:
            datetime_obj: 待处理的datetime对象，不传时默认取当前时间
            format_str: 时间格式化字符串
        """
        self.datetime_obj = datetime_obj or datetime.now()
        self.format_str = format_str

    @property
    def yesterday(self) -> datetime:
        return self._timedelta_calc(days=-1)

    @property
    def tomorrow(self) -> datetime:
        return self._timedelta_calc(days=1)

    @property
    def week_later(self) -> datetime:
        return self._timedelta_calc(days=7)

    def get_n_days_later(self, days: float) -> datetime:
        """
        获取几天前|后的时间
        Args:
            days: 天数时间差, 整数几天后, 负数几天前

        Returns: datetime
        """
        return self._timedelta_calc(days=days)

    def get_n_hours_later(self, hours: float) -> datetime:
        """
        获取几小时前|后的时间
        Args:
            hours: 小时时间差, 整数几小时后, 负数几小时前

        Returns: datetime
        """
        return self._timedelta_calc(hours=hours)

    def _timedelta_calc(self, days: float = 0, hours: float = 0, seconds: float = 0) -> datetime:
        """时间差计算"""
        return self.datetime_obj + timedelta(days=days, hours=hours, seconds=seconds)

    def str_to_datetime(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, self.format_str)

    def datetime_to_str(self) -> str:
        return self.datetime_obj.strftime(self.format_str)

    def timestamp_to_time_str(self, timestamp: float) -> str:
        return time.strftime(self.format_str, time.localtime(timestamp))

    def time_str_to_timestamp(self, time_str: str) -> int:
        return int(time.mktime(time.strptime(time_str, self.format_str)))

    @staticmethod
    def timestamp_to_datetime(timestamp: float) -> datetime:
        return datetime.fromtimestamp(timestamp)

    @property
    def timestamp(self) -> int:
        return int(self.datetime_obj.timestamp())


def main():
    print(TimeUtils().datetime_to_str())
    print(TimeUtils(datetime_obj=datetime.now() + timedelta(days=1)).tomorrow)
    print(TimeUtils().week_later)
    print(TimeUtils().yesterday)
    print(TimeUtils().get_n_days_later(10))

    print(TimeUtils().str_to_datetime("2023-2-05 01:20:30"))
    print(TimeUtils().datetime_to_str())
    print(TimeUtils().timestamp_to_time_str(datetime.now().timestamp()))


if __name__ == '__main__':
    main()
