#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: file.py
# @Desc: { 模块描述 }
# @Date: 2024/07/19 15:44
import mimetypes
import os
from pathlib import Path
from typing import Union


class FileUtil:
    @staticmethod
    def get_file_info(
        filelike: Union[str, bytes, Path],
        filename: str = None,
        only_bytes=True,
    ) -> Union[bytes, tuple]:
        """
        获取文件字节信息
        Args:
            filelike: 文件数据
            filename: 通过字节数据上传需要指定文件名称，方便获取mime_type
            only_bytes: 是否只需要字节数据

        Raises:
            ValueError

        Notes:
            上传文件时指定文件的mime_type

        Returns:
            [bytes, tuple]
        """
        if isinstance(filelike, (str, Path)):
            filename = os.path.basename(str(filelike))
            with open(filelike, "rb") as file:
                file_bytes = file.read()

            if only_bytes:
                return file_bytes

            mime_type = mimetypes.guess_type(filelike)[0]
            return filename, file_bytes, mime_type
        elif isinstance(filelike, bytes):
            if only_bytes:
                return filelike
            if not filename:
                raise ValueError("bytes_filename must be set when passing bytes")

            mime_type = mimetypes.guess_type(filename)[0]
            return filename, filelike, mime_type
        else:
            raise ValueError("filelike must be a string (file path) or bytes.")

    @staticmethod
    def verify_file_ext(filelike: Union[str, bytes, Path], allowed_file_extensions: set, bytes_filename: str = None):
        """
        校验文件后缀
        Args:
            filelike: 文件路径 or 文件字节数据
            allowed_file_extensions: 允许的文件扩展名
            bytes_filename: 当字节数据时使用这个参数校验

        Raises:
            ValueError

        Returns:
        """
        verify_file_path = None
        if isinstance(filelike, (str, Path)):
            verify_file_path = str(filelike)
        elif isinstance(filelike, bytes) and bytes_filename:
            verify_file_path = bytes_filename

        if not verify_file_path:
            # 仅传字节数据数据时不校验
            return

        file_ext = os.path.splitext(verify_file_path)[1].lower()
        if file_ext not in allowed_file_extensions:
            raise ValueError(f"Not allowed {file_ext} File extension must be one of {allowed_file_extensions}")
