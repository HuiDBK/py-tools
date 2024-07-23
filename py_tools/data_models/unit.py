#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: unit.py
# @Desc: { 单位数据模型 }
# @Date: 2024/04/24 11:05
import re


class ByteUnit:
    """字节大小单位"""

    B = 1  # 字节
    KB = 1024 * B  # 千字节 (1 KB = 1024 字节)
    MB = 1024 * KB  # 兆字节 (1 MB = 1024 KB)
    GB = 1024 * MB  # 吉字节 (1 GB = 1024 MB)
    TB = 1024 * GB  # 太字节 (1 TB = 1024 GB)
    PB = 1024 * TB  # 拍字节 (1 PB = 1024 TB)
    EB = 1024 * PB  # 艾字节 (1 EB = 1024 PB)
    ZB = 1024 * EB  # 泽字节 (1 ZB = 1024 EB)
    YB = 1024 * ZB  # 尧字节 (1 YB = 1024 ZB)

    @classmethod
    def convert_size_to_bytes(cls, str_size):
        """
        转换字符串数据大小为字节大小
        Args:
            str_size: 数据大小, eg. 1B, 1kb, 1MB, 1GB

        Returns: int
        """
        str_size = str_size.strip().upper()
        match_ret = re.match(r"^(\d+)(\w+)$", str_size)
        if match_ret:
            num = int(match_ret.group(1))
            unit = match_ret.group(2)
            unit_size = getattr(cls, unit)
            return num * unit_size
        raise ValueError(f"Invalid size format: {str_size}")


class LengthUnit:
    """长度单位"""

    MM = 1  # 毫米
    CM = 10 * MM  # 厘米
    DM = 10 * CM  # 分米
    M = 10 * DM  # 米
    KM = 1000 * M  # 千米
    INCH = 25.4 * MM  # 英寸 (1 英寸 = 25.4 毫米)
    FOOT = 12 * INCH  # 英尺 (1 英尺 = 12 英寸)
    YARD = 3 * FOOT  # 码 (1 码 = 3 英尺)
    MILE = 1760 * YARD  # 英里 (1 英里 = 1760 码)


class WeightUnit:
    """重量单位"""

    MG = 1  # 毫克
    G = 1000 * MG  # 克
    KG = 1000 * G  # 千克
    TONNE = 1000 * KG  # 公吨
    OUNCE = 28.3495 * G  # 盎司 (1 盎司 = 28.3495 克)
    POUND = 16 * OUNCE  # 磅 (1 磅 = 16 盎司)
    STONE = 14 * POUND  # 英石 (1 英石 = 14 磅)
    TON = 2000 * POUND  # 短吨 (1 短吨 = 2000 磅)


class VolumeUnit:
    """容量单位"""

    ML = 1  # 毫升
    L = 1000 * ML  # 升
    CUBIC_METER = 1000 * L  # 立方米
    CUBIC_INCH = 16.387064 * ML  # 立方英寸
    CUBIC_FOOT = 28.3168466 * L  # 立方英尺


class SpeedUnit:
    """速度单位"""

    M_S = 1  # 米每秒
    KM_H = 3.6 * M_S  # 千米每小时
    MPH = 0.44704 * M_S  # 英里每小时


class PowerUnit:
    """功率单位"""

    WATT = 1  # 瓦特
    KW = 1000 * WATT  # 千瓦
    HP = 735.49875 * WATT  # 马力 (1 马力 ≈ 735.49875 瓦特)


class TimeUnit:
    """时间单位"""

    SECOND = 1  # 秒
    MINUTE = 60 * SECOND  # 分钟
    HOUR = 60 * MINUTE  # 小时
    DAY = 24 * HOUR  # 天
    WEEK = 7 * DAY  # 周
    MONTH = 30.44 * DAY  # 月 (平均天数)
    YEAR = 365.24 * DAY  # 年 (平均天数)
    DECADE = 10 * YEAR  # 十年
    CENTURY = 100 * YEAR  # 世纪
