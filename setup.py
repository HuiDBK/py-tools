#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 时间工具类模块 }
# @Date: 2023/9/04 19:59
import operator
from functools import reduce
from setuptools import find_packages, setup


class PKGManager:
    name = "hui-tools"
    version = "0.1.0"
    author = "hui"
    author_email = "huidbk@163.com"

    @classmethod
    def get_pkg_desc(cls):
        """获取包描述"""
        with open("README.md", "r") as f:
            long_description = f.read()
        return long_description

    @classmethod
    def get_install_requires(cls):
        """获取必须安装依赖"""
        requires = [
            "loguru==0.7.0",
            "pydantic==2.1.1"
        ]
        return requires

    @classmethod
    def get_extras_require(cls):
        """
        可选的依赖
        """
        extras_require = {
            "db-orm": ["sqlalchemy[asyncio]==2.0.20", "aiomysql==0.2.0"],
            "db-redis": ["redis==4.5.4", "aioredis==2.0.1"],
            "chatbot": ["requests==2.31.0", "cacheout==0.14.1"],
            "http-client": ["httpx==0.24.1", "requests==2.31.0"],
            "time-tools": ["python-dateutil==2.8.2"],
            "excel-tools": ["pandas==1.3.5", "openpyxl==3.0.10"],
        }

        extras_require["all"] = list(
            set(reduce(operator.add, [cls.get_install_requires(), *extras_require.values()]))
        )
        return extras_require


def main():

    setup(
        name=PKGManager.name,
        author=PKGManager.author,
        author_email=PKGManager.author_email,
        version=PKGManager.version,
        packages=find_packages(),
        url="https://github.com/HuiDBK/py-tools",
        license="Apache",
        long_description=PKGManager.get_pkg_desc(),
        long_description_content_type="text/markdown",
        install_requires=PKGManager.get_install_requires(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
        ],
        extras_require=PKGManager.get_extras_require(),
        python_requires=">=3.7"
    )


if __name__ == '__main__':
    # python3 setup.py sdist bdist_wheel
    # twine upload --repository testpypi dist/*
    # twine upload dist/*
    main()
