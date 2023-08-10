#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 时间工具类案例 }
# @Date: 2023/04/30 21:08
import time
from datetime import datetime

from py_tools.utils import TimeUtil


def time_util_demo():
    # 创建一个TimeUtil实例，默认使用当前时间
    time_util = TimeUtil()

    print("昨天的日期:", time_util.yesterday)

    print("明天的日期:", time_util.tomorrow)

    print("一周后的日期:", time_util.week_later)

    print("一个月后的日期:", time_util.month_later)

    # 从现在开始增加10天
    print("10天后的日期:", time_util.add_time(days=10))

    # 从现在开始减少5天
    print("5天前的日期:", time_util.sub_time(days=5))

    date_str = "2023-05-01 12:00:00"
    print("字符串转换为datetime对象:", time_util.str_to_datetime(date_str))

    print("datetime对象转换为字符串:", time_util.datetime_to_str())

    timestamp = time.time()
    print("时间戳转换为时间字符串:", time_util.timestamp_to_str(timestamp))

    time_str = "2023-05-01 12:00:00"
    print("时间字符串转换为时间戳:", time_util.str_to_timestamp(time_str))

    print("时间戳转换为datetime对象:", time_util.timestamp_to_datetime(timestamp))

    print("当前时间的时间戳:", time_util.timestamp)

    date1 = datetime(2023, 4, 24)  # 2023年4月24日，星期一
    date2 = datetime(2023, 5, 1)  # 2023年5月1日，星期一
    time_util = TimeUtil(datetime_obj=date1)

    # 计算两个日期之间的工作日数量
    weekday_count = time_util.count_weekdays_between(date2, include_end_date=True)
    print(f"从 {date1} 到 {date2} 之间有 {weekday_count} 个工作日。(包含末尾日期)")

    weekday_count = time_util.count_weekdays_between(date2, include_end_date=False)
    print(f"从 {date1} 到 {date2} 之间有 {weekday_count} 个工作日。(不包含末尾日期)")

    # 获取两个日期之间的差值
    date_diff = time_util.difference_in_detail(date2)
    print(date_diff)


def main():
    time_util_demo()


if __name__ == "__main__":
    main()
