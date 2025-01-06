#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: test_file_util.py
# @Desc: { 文件工具类单测 }
# @Date: 2025/01/06 14:10
from PIL import ImageFilter

from py_tools.constants import DEMO_DATA
from py_tools.utils import ImageUtil

DATA_IMAGE_DIR = DEMO_DATA.joinpath("images")
DATA_TEMP_DIR = DEMO_DATA.joinpath("tmp")


class TestImageUtil:
    def setup(self):
        self.sample_image = DATA_IMAGE_DIR / "sample.jpeg"

    def test_resize_image(self):
        tmp_out_image = DATA_TEMP_DIR / "test_tmp.jpg"
        new_size = (200, 200)
        result = ImageUtil.resize_image(self.sample_image, tmp_out_image, size=new_size)

        assert result is None
        img_size = ImageUtil.get_image_resolution(tmp_out_image)
        assert img_size == new_size

    def test_crop_image(self):
        result = ImageUtil.crop_image(self.sample_image, crop_box=(10, 10, 100, 100))
        assert isinstance(result, bytes)

    def test_enhance_image(self):
        result = ImageUtil.enhance_image(self.sample_image, factor=2.0)
        assert isinstance(result, bytes)

    def test_apply_filter(self):
        result = ImageUtil.apply_filter(self.sample_image, filter_type=ImageFilter.MaxFilter)
        assert isinstance(result, bytes)

    def test_convert_to_grayscale(self):
        result = ImageUtil.convert_to_grayscale(self.sample_image)
        assert isinstance(result, bytes)

    def test_convert_image_format(self):
        result = ImageUtil.convert_image_format(self.sample_image, "PNG")
        assert isinstance(result, bytes)

    def test_get_image_resolution(self):
        resolution = ImageUtil.get_image_resolution(self.sample_image)
        assert isinstance(resolution, tuple)
        assert len(resolution) == 2
