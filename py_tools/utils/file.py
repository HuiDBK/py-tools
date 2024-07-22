#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: file.py
# @Desc: { 文件相关工具模块 }
# @Date: 2024/07/19 15:44
import mimetypes
import os
from pathlib import Path
from typing import AsyncGenerator, Generator, Union

import aiofiles


class FileUtil:
    @staticmethod
    def get_file_info(
        file_input: Union[str, bytes, Path],
        filename: str = None,
    ) -> Union[bytes, tuple]:
        """
        获取文件字节信息
        Args:
            file_input: 文件数据
            filename: 通过字节数据上传需要指定文件名称，方便获取mime_type

        Raises:
            ValueError

        Notes:
            上传文件时指定文件的mime_type

        Returns:
            tuple(filename, file_bytes, mime_type)
        """
        if isinstance(file_input, (str, Path)):
            filename = os.path.basename(str(file_input))
            with open(file_input, "rb") as file:
                file_bytes = file.read()

            mime_type = mimetypes.guess_type(file_input)[0]
            return filename, file_bytes, mime_type
        elif isinstance(file_input, bytes):
            if not filename:
                raise ValueError("filename must be set when passing bytes")

            mime_type = mimetypes.guess_type(filename)[0]
            return filename, file_input, mime_type
        else:
            raise ValueError("file_input must be a string (file path) or bytes.")

    @staticmethod
    def verify_file_ext(file_input: Union[str, bytes, Path], allowed_file_extensions: set, bytes_filename: str = None):
        """
        校验文件后缀
        Args:
            file_input: 文件路径 or 文件字节数据
            allowed_file_extensions: 允许的文件扩展名
            bytes_filename: 当字节数据时使用这个参数校验

        Raises:
            ValueError

        Returns:
        """
        verify_file_path = None
        if isinstance(file_input, (str, Path)):
            verify_file_path = str(file_input)
        elif isinstance(file_input, bytes) and bytes_filename:
            verify_file_path = bytes_filename

        if not verify_file_path:
            # 仅传字节数据数据时不校验
            return

        file_ext = os.path.splitext(verify_file_path)[1].lower()
        if file_ext not in allowed_file_extensions:
            raise ValueError(f"Not allowed {file_ext} File extension must be one of {allowed_file_extensions}")

    @staticmethod
    async def aread_bytes(file_path: Union[str, Path]) -> bytes:
        """
        异步读取文件的字节数据。

        Args:
            file_path: 要读取的文件路径。

        Raises:
            ValueError: 如果提供的路径不是字符串或Path对象。

        Returns:
            bytes: 文件的全部字节数据。
        """
        if not isinstance(file_path, (str, Path)):
            raise ValueError("file_path必须是字符串或Path对象")

        async with aiofiles.open(file_path, "rb") as file:
            file_bytes = await file.read()
        return file_bytes

    @staticmethod
    def read_bytes_chunked(file_path: Union[str, Path], chunk_size: int = 1024) -> Generator:
        """
        同步分块读取文件字节数据。

        Args:
            file_path: 要读取的文件路径。
            chunk_size: 每块读取的字节数，默认1024字节。

        Raises:
            ValueError: 如果提供的路径不是字符串或Path对象。

        Returns:
            生成器: 每次迭代返回一个字节数据块。
        """
        if not isinstance(file_path, (str, Path)):
            raise ValueError("file_path必须是字符串或Path对象")

        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    @staticmethod
    async def aread_bytes_chunked(file_path: Union[str, Path], chunk_size: int = 1024) -> AsyncGenerator[bytes, None]:
        """
        异步分块读取文件字节数据。

        Args:
            file_path: 要读取的文件路径。
            chunk_size: 每块读取的字节数，默认1024字节。

        Raises:
            ValueError: 如果提供的路径不是字符串或Path对象。

        Returns:
            异步生成器: 每次迭代返回一个字节数据块。
        """
        if not isinstance(file_path, (str, Path)):
            raise ValueError("file_path必须是字符串或Path对象")

        async with aiofiles.open(file_path, "rb") as file:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                yield chunk


async def main():
    file_bytes = await FileUtil.aread_bytes(Path(__file__))
    print(file_bytes)

    for chunk in FileUtil.read_bytes_chunked(Path(__file__), chunk_size=1024):
        print(chunk)

    async for chunk in FileUtil.aread_bytes_chunked(Path(__file__), chunk_size=1024):
        print(chunk)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
