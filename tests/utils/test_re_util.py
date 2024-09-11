#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: test_re_util.py
# @Desc: { RegexUtil unitest }
# @Date: 2024/09/11 15:47
from py_tools.utils import RegexUtil


class TestRegexUtil:
    """RegexUtil 单元测试类"""

    def test_find_http_links(self):
        """测试 HTTP 链接的匹配"""
        text = "访问 https://www.juejin.cn 或 http://example.com 了解更多信息。"
        expected = ["https://www.juejin.cn", "http://example.com"]
        assert RegexUtil.find_http_links(text) == expected

    def test_find_chinese_characters(self):
        """测试中文字符的匹配"""
        text = "这是一个测试"
        expected = ["这", "是", "一", "个", "测", "试"]
        assert RegexUtil.find_chinese_characters(text) == expected

    def test_find_double_byte_characters(self):
        """测试双字节字符的匹配"""
        text = "ｔｅｓｔ这是测试"
        expected = ["ｔ", "ｅ", "ｓ", "ｔ", "这", "是", "测", "试"]
        assert RegexUtil.find_double_byte_characters(text) == expected

    def test_find_emails(self):
        """测试 Email 地址的匹配"""
        text = "联系我: huidbk@example.com, hui@domain.cn"
        expected = ["huidbk@example.com", "hui@domain.cn"]
        assert RegexUtil.find_emails(text) == expected

    def test_find_chinese_phone_numbers(self):
        """测试中国大陆手机号码的匹配"""
        text = "我的手机号是13800138000，朋友的手机号是14712345678"
        expected = ["13800138000", "14712345678"]
        assert RegexUtil.find_chinese_phone_numbers(text) == expected

    def test_find_qq_numbers(self):
        """测试腾讯QQ号的匹配"""
        text = "我的QQ号是123456789，朋友的QQ号是987654321"
        expected = ["123456789", "987654321"]
        assert RegexUtil.find_qq_numbers(text) == expected

    def test_find_postal_codes(self):
        """测试邮政编码的匹配"""
        text = "我的邮政编码是123456"
        expected = ["123456"]
        assert RegexUtil.find_postal_codes(text) == expected

    def test_find_dates(self):
        """测试日期格式的匹配"""
        text = "今天的日期是2024-08-24，昨天是2024/08/23"
        expected = ["2024-08-24", "2024/08/23"]
        assert RegexUtil.find_dates(text) == expected

    def test_find_integers(self):
        """测试整数的匹配"""
        text = "正数: 123, 负数: -456"
        expected = ["123", "-456"]
        assert RegexUtil.find_integers(text) == expected

    def test_find_positive_floats(self):
        """测试正浮点数的匹配"""
        text = "正浮点数: 12.34, 0.56"
        expected = ["12.34", "0.56"]
        assert RegexUtil.find_positive_floats(text) == expected

    def test_find_negative_floats(self):
        """测试负浮点数的匹配"""
        text = "负浮点数: -12.34, -0.56，负整数 -100"
        expected = ["-12.34", "-0.56"]
        assert RegexUtil.find_negative_floats(text) == expected

    def test_find_usernames(self):
        """测试用户名的匹配"""
        text = "user123, 张三_001"
        expected = ["user123", "张三_001"]
        assert RegexUtil.find_usernames(text) == expected
