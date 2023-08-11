#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 时间工具类模块 }
# @Date: 2022/11/26 16:08

import time
from datetime import datetime
from typing import Type

from dateutil.relativedelta import relativedelta

from py_tools.data_models.time import DateDiff
from py_tools.meta_cls import SingletonMetaCls
from py_tools.enums import TimeFormatEnum


class TimeUtil(metaclass=SingletonMetaCls):
    """
    时间工具类
    """

    @classmethod
    def instance(cls, reinit=True, *args, **kwargs):
        instance: Type[cls] = cls._init_instance()
        if reinit:
            instance.__init__(*args, **kwargs)
        return instance

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
        """获取昨天的日期"""
        return self.sub_time(days=1)

    @property
    def tomorrow(self) -> datetime:
        """获取明天的日期"""
        return self.add_time(days=1)

    @property
    def week_later(self) -> datetime:
        """获取一周后的日期"""
        return self.add_time(days=7)

    @property
    def month_later(self) -> datetime:
        """获取一个月后的日期"""
        return self.add_time(months=1)

    def add_time(self, years=0, months=0, days=0, hours=0, minutes=0, seconds=0, **kwargs) -> datetime:
        """增加指定时间"""
        return self.datetime_obj + relativedelta(
            years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds, **kwargs
        )

    def sub_time(self, years=0, months=0, days=0, hours=0, minutes=0, seconds=0, **kwargs) -> datetime:
        """减去指定时间"""
        return self.datetime_obj - relativedelta(
            years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds, **kwargs
        )

    def str_to_datetime(self, date_str: str, format_str: str = None) -> datetime:
        """将时间字符串转换为 datetime 对象"""
        format_str = format_str or self.format_str
        return datetime.strptime(date_str, format_str)

    def datetime_to_str(self, format_str: str = None) -> str:
        """将 datetime 对象转换为时间字符串"""
        format_str = format_str or self.format_str
        return self.datetime_obj.strftime(format_str)

    def timestamp_to_str(self, timestamp: float, format_str: str = None) -> str:
        """将时间戳转换为时间字符串"""
        format_str = format_str or self.format_str
        return datetime.fromtimestamp(timestamp).strftime(format_str)

    def str_to_timestamp(self, time_str: str, format_str: str = None) -> float:
        """将时间字符串转换为时间戳"""
        format_str = format_str or self.format_str
        return time.mktime(time.strptime(time_str, format_str))

    @staticmethod
    def timestamp_to_datetime(timestamp: float) -> datetime:
        """将时间戳转换为 datetime 对象"""
        return datetime.fromtimestamp(timestamp)

    @property
    def timestamp(self) -> float:
        """获取 datetime 对象的时间戳"""
        return self.datetime_obj.timestamp()

    def difference_in_detail(self, datetime_obj: datetime):
        """
        计算两个日期之间的差值详情
        Args:
            datetime_obj: 时间对象

        Returns: DateDiff
        """
        delta = relativedelta(self.datetime_obj, datetime_obj)

        return DateDiff(
            years=abs(delta.years),
            months=abs(delta.months),
            days=abs(delta.days),
            hours=abs(delta.hours),
            minutes=abs(delta.minutes),
            seconds=abs(delta.seconds),
        )

    def start_of_week(self) -> datetime:
        """获取本周的开始日期（周一）"""
        return self.datetime_obj - relativedelta(days=self.datetime_obj.weekday())

    def end_of_week(self) -> datetime:
        """获取本周的结束日期（周日）"""
        return self.start_of_week() + relativedelta(days=6)

    def start_of_month(self) -> datetime:
        """获取本月的第一天"""
        return self.datetime_obj.replace(day=1)

    def end_of_month(self) -> datetime:
        """获取本月的最后一天"""
        next_month = self.add_time(months=1)
        return next_month.replace(day=1) - relativedelta(days=1)

    def start_of_quarter(self) -> datetime:
        """获取本季度的第一天"""
        quarter_month_start = (self.datetime_obj.month - 1) // 3 * 3 + 1
        return self.datetime_obj.replace(month=quarter_month_start, day=1)

    def end_of_quarter(self) -> datetime:
        """获取本季度的最后一天"""
        next_quarter_start = self.start_of_quarter().replace(month=self.datetime_obj.month + 3)
        return next_quarter_start - relativedelta(days=1)

    def start_of_year(self) -> datetime:
        """获取本年度的第一天"""
        return self.datetime_obj.replace(month=1, day=1)

    def end_of_year(self) -> datetime:
        """获取本年度的最后一天"""
        return self.datetime_obj.replace(month=12, day=31)

    def is_weekday(self) -> bool:
        """判断当前日期是否是工作日（星期一到星期五）"""
        return self.datetime_obj.weekday() < 5

    def count_weekdays_between(self, datetime_obj: datetime, include_end_date: bool = True) -> int:
        """计算两个日期之间的工作日数量

        Args:
            datetime_obj: datetime 对象
            include_end_date: 是否包含结束日期（默认为 True）

        Returns:
            两个日期之间的工作日数量
        """
        # 确保 start_date 是较小的日期，end_date 是较大的日期
        start_date = min(self.datetime_obj, datetime_obj)
        end_date = max(self.datetime_obj, datetime_obj)

        # 如果不包含结束日期，将 end_date 减去一天
        if not include_end_date:
            end_date = end_date - relativedelta(days=1)

        # 计算两个日期之间的天数
        days_between = abs((end_date - start_date).days)

        # 计算完整周数，每周有5个工作日
        weeks_between = days_between // 7
        weekdays = weeks_between * 5

        # 计算剩余的天数
        remaining_days = days_between % 7
        # 遍历剩余的天数，检查每天是否为工作日，如果是，则累加工作日数量
        for day_offset in range(remaining_days + 1):
            if (start_date + relativedelta(days=day_offset)).weekday() < 5:
                weekdays += 1

        return weekdays
