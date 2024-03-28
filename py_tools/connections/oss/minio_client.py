#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { minio客户端模块 }
# @Date: 2023/11/07 17:41
from datetime import timedelta
from io import BytesIO

from minio import Minio


class MinioClient(Minio):
    """
    自定义的 MinIO 客户端类，继承自 Minio 类。
    """

    def __init__(self, endpoint, access_key, secret_key, secure=False, **kwargs):
        """
        初始化 MinioClient 对象。
        Args:
            endpoint: MinIO 服务器的终端节点
            access_key: MinIO 访问密钥
            secret_key: MinIO 秘密密钥
            secure: 是否使用安全连接，默认为 False
            **kwargs: 其他关键字参数
        """
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure

        super().__init__(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            **kwargs
        )

    def put_object_get_sign_url(
            self,
            bucket_name: str,
            object_name: str,
            data: bytes,
            content_type: str = "application/octet-stream",
            sign_expires=timedelta(days=1),
            **kwargs
    ):
        """
        上传对象并获取预签名 URL。
        Args:
            bucket_name: 存储桶名称
            object_name: 对象名称
            data: 字节数据
            content_type: 对象的内容类型
            sign_expires: 对象签名过期时间，默认为 1 天
            **kwargs: 其他关键字参数

        Returns:
            预签名 URL
        """
        data_size = len(data)
        self.put_object(bucket_name, object_name, BytesIO(data), data_size, content_type, **kwargs)

        obj_sign_url = self.presigned_get_object(bucket_name, object_name, expires=sign_expires)
        return obj_sign_url
