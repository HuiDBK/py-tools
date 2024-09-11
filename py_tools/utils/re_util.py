#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: re_util.py
# @Desc: { 正则工具模块 }
# @Date: 2024/08/24 11:31
import re
from typing import List


class RegexUtil:
    """正则工具类"""

    # 匹配中文字符
    CHINESE_CHARACTER_PATTERN = re.compile(r"[\u4e00-\u9fa5]")

    # 匹配双字节字符（包括汉字以及其他全角字符）
    DOUBLE_BYTE_CHARACTER_PATTERN = re.compile(r"[^\x00-\xff]")

    # 匹配Email地址
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    # 匹配http网址URL
    HTTP_LINK_PATTERN = re.compile(r"(https?:\/\/\S+)")

    # 匹配中国大陆手机号码
    CHINESE_PHONE_PATTERN = re.compile(r"1[3-9]\d{9}")

    # 匹配电话号码（包括座机）
    TELEPHONE_PATTERN = re.compile(r"[0-9-()（）]{7,18}")

    # 匹配负浮点数
    NEGATIVE_FLOAT_PATTERN = re.compile(r"-?\d+\.\d+")

    # 匹配整数（包括正负）
    INTEGER_PATTERN = re.compile(r"-?[1-9]\d*")

    # 匹配正浮点数
    POSITIVE_FLOAT_PATTERN = re.compile(r"[1-9]\d*\.\d*|0\.\d*[1-9]\d*")

    # 匹配腾讯QQ号
    QQ_PATTERN = re.compile(r"\d{5,11}")

    # 匹配中国邮政编码
    POSTAL_CODE_PATTERN = re.compile(r"\d{6}")

    # 匹配中国身份证号码
    ID_CARD_PATTERN = re.compile(r"\d{17}[\d|x]|\d{15}")

    # 匹配日期格式（如YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD）
    DATE_PATTERN = re.compile(r"\d{4}[-/.]\d{2}[-/.]\d{2}")

    # 匹配正整数
    POSITIVE_INTEGER_PATTERN = re.compile(r"[1-9]\d*")

    # 匹配负整数
    NEGATIVE_INTEGER_PATTERN = re.compile(r"-[1-9]\d*")

    # 匹配用户名（支持中英文、数字、下划线、减号）
    USERNAME_PATTERN = re.compile(r"[A-Za-z0-9_\-\u4e00-\u9fa5]+")

    @classmethod
    def find_http_links(cls, text: str) -> List[str]:
        """查找文本中的所有HTTP/HTTPS链接"""
        return cls.HTTP_LINK_PATTERN.findall(text)

    @classmethod
    def find_chinese_characters(cls, text: str) -> List[str]:
        """查找文本中的所有中文字符"""
        return cls.CHINESE_CHARACTER_PATTERN.findall(text)

    @classmethod
    def find_double_byte_characters(cls, text: str) -> List[str]:
        """查找文本中的所有双字节字符"""
        return cls.DOUBLE_BYTE_CHARACTER_PATTERN.findall(text)

    @classmethod
    def find_emails(cls, text: str) -> List[str]:
        """查找文本中的所有Email地址"""
        return cls.EMAIL_PATTERN.findall(text)

    @classmethod
    def find_chinese_phone_numbers(cls, text: str) -> List[str]:
        """查找文本中的所有中国大陆手机号码"""
        return cls.CHINESE_PHONE_PATTERN.findall(text)

    # 查找所有匹配的电话号码（包括座机）
    @classmethod
    def find_telephone_numbers(cls, text: str) -> List[str]:
        """查找文本中的所有电话号码（包括座机）"""
        return cls.TELEPHONE_PATTERN.findall(text)

    @classmethod
    def find_negative_floats(cls, text: str) -> List[str]:
        """查找文本中的所有负浮点数"""
        return cls.NEGATIVE_FLOAT_PATTERN.findall(text)

    @classmethod
    def find_integers(cls, text: str) -> List[str]:
        """查找文本中的所有整数（包括正负）"""
        return cls.INTEGER_PATTERN.findall(text)

    @classmethod
    def find_positive_floats(cls, text: str) -> List[str]:
        """查找文本中的所有正浮点数"""
        return cls.POSITIVE_FLOAT_PATTERN.findall(text)

    @classmethod
    def find_qq_numbers(cls, text: str) -> List[str]:
        """查找文本中的所有腾讯QQ号"""
        return cls.QQ_PATTERN.findall(text)

    @classmethod
    def find_postal_codes(cls, text: str) -> List[str]:
        """查找文本中的所有邮政编码"""
        return cls.POSTAL_CODE_PATTERN.findall(text)

    @classmethod
    def find_id_cards(cls, text: str) -> List[str]:
        """查找文本中的所有身份证号码"""
        return cls.ID_CARD_PATTERN.findall(text)

    @classmethod
    def find_dates(cls, text: str) -> List[str]:
        """查找文本中的所有日期格式（YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD）"""
        return cls.DATE_PATTERN.findall(text)

    @classmethod
    def find_positive_integers(cls, text: str) -> List[str]:
        """查找文本中的所有正整数"""
        return cls.POSITIVE_INTEGER_PATTERN.findall(text)

    @classmethod
    def find_negative_integers(cls, text: str) -> List[str]:
        """查找文本中的所有负整数"""
        return cls.NEGATIVE_INTEGER_PATTERN.findall(text)

    @classmethod
    def find_usernames(cls, text: str) -> List[str]:
        """查找文本中的所有用户名（支持中英文、数字、下划线、减号）"""
        return cls.USERNAME_PATTERN.findall(text)
