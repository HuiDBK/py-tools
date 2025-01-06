#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: file_util_demo.py
# @Desc: { 模块描述 }
# @Date: 2025/01/06 13:37
import os

from py_tools.constants import DEMO_DATA
from py_tools.utils import ImageUtil

DATA_IMAGE_DIR = DEMO_DATA.joinpath("images")
DATA_TEMP_DIR = DEMO_DATA.joinpath("tmp")


def main():
    # 示例 1: 调整图像大小
    input_path = DATA_IMAGE_DIR / "sample.jpeg"
    output_path = DATA_TEMP_DIR / "resized_sample.jpg"
    img_bytes = ImageUtil.resize_image(input_path, size=(500, 500))
    os.makedirs(DATA_TEMP_DIR, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    # 示例 2: 图像裁剪
    crop_output = DATA_TEMP_DIR / "cropped_sample.jpg"
    ImageUtil.crop_image(input_path, crop_output, crop_box=(300, 300, 800, 800))

    # 示例 3: 增强图像锐度
    enhance_output = DATA_TEMP_DIR / "enhanced_sample.jpg"
    ImageUtil.enhance_image(input_path, enhance_output, factor=1.5)

    # 示例 4: 应用滤镜
    filter_output = DATA_TEMP_DIR / "filtered_sample.jpg"
    ImageUtil.apply_filter(input_path, filter_output)

    # 示例 5: 转换为灰度图像
    gray_output = DATA_TEMP_DIR / "gray_sample.jpg"
    ImageUtil.convert_to_grayscale(input_path, gray_output)

    # 示例 6: 转换图像格式
    format_output = DATA_TEMP_DIR / "converted_sample.png"
    ImageUtil.convert_image_format(input_path, "png", format_output)

    # 示例 7: 获取图像分辨率
    resolution = ImageUtil.get_image_resolution(input_path)
    print(f"图像分辨率: {resolution}")


if __name__ == "__main__":
    main()
