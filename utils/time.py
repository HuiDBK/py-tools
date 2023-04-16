#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 时间工具类模块 }
# @Date: 2022/11/26 16:08

import time
from datetime import datetime

from dateutil.relativedelta import relativedelta

from enums.time import TimeFormatEnum


class TimeUtil(object):

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
        return self.sub_time(days=1)

    @property
    def tomorrow(self) -> datetime:
        return self.add_time(days=1)

    @property
    def week_later(self) -> datetime:
        return self.add_time(days=7)

    @property
    def month_later(self) -> datetime:
        return self.add_time(months=1)

    def add_time(self, months=0, days=0, hours=0, minutes=0, seconds=0, **kwargs):
        return self.datetime_obj + relativedelta(
            months=months, days=days, hours=hours, minutes=minutes, seconds=seconds, **kwargs
        )

    def sub_time(self, months=0, days=0, hours=0, minutes=0, seconds=0, **kwargs):
        return self.datetime_obj - relativedelta(
            months=months, days=days, hours=hours, minutes=minutes, seconds=seconds, **kwargs
        )

    def str_to_datetime(self, date_str: str, format_str: str = None) -> datetime:
        format_str = format_str or self.format_str
        return datetime.strptime(date_str, format_str)

    def datetime_to_str(self, format_str: str = None) -> str:
        format_str = format_str or self.format_str
        return self.datetime_obj.strftime(format_str)

    def timestamp_to_time_str(self, timestamp: float, format_str: str = None) -> str:
        format_str = format_str or self.format_str
        return datetime.fromtimestamp(timestamp).strftime(format_str)

    def time_str_to_timestamp(self, time_str: str, format_str: str = None) -> int:
        format_str = format_str or self.format_str
        return int(time.mktime(time.strptime(time_str, format_str)))

    @staticmethod
    def timestamp_to_datetime(timestamp: float) -> datetime:
        return datetime.fromtimestamp(timestamp)

    @property
    def timestamp(self) -> int:
        return int(self.datetime_obj.timestamp())


def main():
    print(TimeUtil().datetime_to_str())
    print(TimeUtil(datetime_obj=datetime.now() + relativedelta(days=1)).tomorrow)
    print(TimeUtil().week_later)
    print(TimeUtil().yesterday)
    print(TimeUtil().month_later)
    print(TimeUtil().add_time(10))

    print(TimeUtil().str_to_datetime("2023-2-05 01:20:30"))
    print(TimeUtil().datetime_to_str())
    print(TimeUtil().timestamp_to_time_str(datetime.now().timestamp()))


if __name__ == '__main__':
    main()
