#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: file.py
# @Desc: { 文件相关工具模块 }
# @Date: 2024/07/19 15:44
import mimetypes
import os
from io import BytesIO
from pathlib import Path
from typing import AsyncGenerator, Generator, Union

import aiofiles
from PIL import Image, ImageEnhance, ImageFilter


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
    async def awrite(file_path: Union[str, Path], data: bytes) -> str:
        """
        异步写入文件。

        Args:
            file_path: 要读取的文件路径。
            data: 要写入的字节数据。

        Raises:
            ValueError: 如果提供的路径不是字符串或Path对象。

        Returns:
            file_path: 文件路径。
        """
        if not isinstance(file_path, (str, Path)):
            raise ValueError("file_path必须是字符串或Path对象")

        async with aiofiles.open(file_path, "wb") as file:
            await file.write(data)
        return file_path

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


class ImageUtil(FileUtil):
    @staticmethod
    def _load_image(input_source: str | bytes | Path) -> Image:
        """
        从各种输入源加载图像。

        参数:
            input_source (str | bytes | Path): 图像文件路径、图像字节流或Path对象。

        返回:
            Image: 加载的PIL图像对象。
        """
        if isinstance(input_source, bytes):
            return Image.open(BytesIO(input_source))
        elif isinstance(input_source, (str, Path)):
            return Image.open(input_source)
        else:
            raise ValueError("不支持的输入类型。")

    @staticmethod
    def resize_image(
        input_source: str | bytes | Path, output_path: str | Path = None, size: tuple = (100, 100)
    ) -> bytes | None:
        """
        将图像调整为指定大小。

        参数:
            input_source (str | bytes | Path): 图像文件路径、图像字节流或Path对象。
            output_path (str | Path, 可选): 保存调整大小后图像的路径。默认为None。
            size (tuple): 调整后的宽度和高度 (width, height)。

        返回:
            bytes | None: 如果未提供output_path，返回调整大小的图像字节流，否则返回None。
        """
        with ImageUtil._load_image(input_source) as img:
            img_resized = img.resize(size)
            if output_path:
                img_resized.save(output_path)
            else:
                img_byte_arr = BytesIO()
                img_resized.save(img_byte_arr, format=img.format)
                return img_byte_arr.getvalue()

    @staticmethod
    def crop_image(
        input_source: str | bytes | Path, output_path: str | Path = None, crop_box: tuple = (0, 0, 100, 100)
    ) -> bytes | None:
        """
        按照指定的区域裁剪图像。

        参数:
            input_source (str | bytes | Path): 图像文件路径、图像字节流或Path对象。
            output_path (str | Path, 可选): 保存裁剪后图像的路径。默认为None。
            crop_box (tuple): 裁剪框 (左，上，右，下)。

        返回:
            bytes | None: 如果未提供output_path，返回裁剪后的图像字节流，否则返回None。
        """
        with ImageUtil._load_image(input_source) as img:
            img_cropped = img.crop(crop_box)
            if output_path:
                img_cropped.save(output_path)
            else:
                img_byte_arr = BytesIO()
                img_cropped.save(img_byte_arr, format=img.format)
                return img_byte_arr.getvalue()

    @staticmethod
    def enhance_image(
        input_source: str | bytes | Path, output_path: str | Path = None, factor: float = 1.0
    ) -> bytes | None:
        """
        通过调整锐度增强图像。

        参数:
            input_source (str | bytes | Path): 图像文件路径、图像字节流或Path对象。
            output_path (str | Path, 可选): 保存增强后图像的路径。默认为None。
            factor (float): 增强因子，1.0表示原始图像。

        返回:
            bytes | None: 如果未提供output_path，返回增强后的图像字节流，否则返回None。
        """
        with ImageUtil._load_image(input_source) as img:
            enhancer = ImageEnhance.Sharpness(img)
            img_enhanced = enhancer.enhance(factor)
            if output_path:
                img_enhanced.save(output_path)
            else:
                img_byte_arr = BytesIO()
                img_enhanced.save(img_byte_arr, format=img.format)
                return img_byte_arr.getvalue()

    @staticmethod
    def apply_filter(
        input_source: str | bytes | Path, output_path: str | Path = None, filter_type: ImageFilter = ImageFilter.BLUR
    ) -> bytes | None:
        """
        为图像应用滤镜。

        参数:
            input_source (str | bytes | Path): 图像文件路径、图像字节流或Path对象。
            output_path (str | Path, 可选): 保存应用滤镜后图像的路径。默认为None。
            filter_type (ImageFilter): 要应用的滤镜 (例如BLUR, CONTOUR, DETAIL, EDGE_ENHANCE)。

        返回:
            bytes | None: 如果未提供output_path，返回应用滤镜的图像字节流，否则返回None。
        """
        with ImageUtil._load_image(input_source) as img:
            img_filtered = img.filter(filter_type)
            if output_path:
                img_filtered.save(output_path)
            else:
                img_byte_arr = BytesIO()
                img_filtered.save(img_byte_arr, format=img.format)
                return img_byte_arr.getvalue()

    @staticmethod
    def convert_to_grayscale(input_source: str | bytes | Path, output_path: str | Path = None) -> bytes | None:
        """
        将图像转换为灰度。

        参数:
            input_source (str | bytes | Path): 图像文件路径、图像字节流或Path对象。
            output_path (str | Path, 可选): 保存灰度图像的路径。默认为None。

        返回:
            bytes | None: 如果未提供output_path，返回灰度图像的字节流，否则返回None。
        """
        with ImageUtil._load_image(input_source) as img:
            img_gray = img.convert("L")
            if output_path:
                img_gray.save(output_path)
            else:
                img_byte_arr = BytesIO()
                img_gray.save(img_byte_arr, format=img.format)
                return img_byte_arr.getvalue()

    @staticmethod
    def get_image_resolution(input_source: str | bytes | Path) -> tuple:
        """
        获取图像的分辨率。

        参数:
            input_source (str | bytes | Path): 图像文件路径、图像字节流或Path对象。

        返回:
            tuple: 图像分辨率 (宽度, 高度)。
        """
        with ImageUtil._load_image(input_source) as img:
            return img.size

    @staticmethod
    def convert_image_format(
        input_source: str | bytes | Path, output_format: str, output_path: str | Path = None
    ) -> bytes | None:
        """
        转换图像格式。

        参数:
            input_source (str | bytes | Path): 图像文件路径、图像字节流或Path对象。
            output_format (str): 目标格式 (例如 'JPEG', 'PNG', 'BMP')。
            output_path (str | Path, 可选): 保存转换后图像的路径。默认为None。

        返回:
            bytes | None: 如果未提供output_path，返回转换后的图像字节流，否则返回None。
        """
        with ImageUtil._load_image(input_source) as img:
            if output_path:
                img.save(output_path, format=output_format)
            else:
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format=output_format)
                return img_byte_arr.getvalue()


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
