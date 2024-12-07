#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 序列化器模块 }
# @Date: 2023/09/10 00:15
import dataclasses
from dataclasses import asdict, dataclass
from typing import List, Type, Union

from pydantic import BaseModel
from sqlalchemy import RowMapping

from py_tools.connections.db.mysql import BaseOrmTable


class SerializerUtil:
    @classmethod
    def data_to_model(
        cls,
        data_obj: Union[
            dict,
            BaseOrmTable,
            BaseModel,
            dataclass,
            List[dict],
            List[BaseOrmTable],
            List[BaseModel],
        ],
        to_model: Type[Union[BaseModel, BaseOrmTable, dataclass]],
    ) -> Union[BaseModel, List[BaseModel], List[BaseOrmTable], List[dataclass], None]:
        """
        将数据对象转换成 pydantic 或 sqlalchemy 模型对象, 如果是数据库库表模型对象则调用to_dict()后递归
        Args:
            data_obj: 支持 字典对象, pydantic、sqlalchemy模型对象, 列表对象
            to_model: 转换后数据模型

        Notes:
            - 对于实现了 to_dict() 方法的模型对象，将调用该方法返回字典。

        returns:
            转换后的对象
        """

        if isinstance(data_obj, dict):
            # 字典处理
            return to_model(**data_obj)

        elif isinstance(data_obj, BaseOrmTable):
            # 数据库表模型对象处理, to_dict()后递归调用
            return cls.data_to_model(data_obj.to_dict(), to_model=to_model)

        elif isinstance(data_obj, BaseModel):
            # pydantic v2 模型对象处理, model_dump 后递归调用
            return cls.data_to_model(data_obj.model_dump(), to_model=to_model)

        elif dataclasses.is_dataclass(data_obj):
            # dataclass 模型对象处理, asdict() 后递归调用
            return cls.data_to_model(asdict(data_obj), to_model=to_model)

        elif hasattr(data_obj, "to_dict"):
            # 如果模型对象有 to_dict 方法，调用该方法返回字典
            return cls.data_to_model(data_obj.to_dict(), to_model=to_model)

        elif isinstance(data_obj, list):
            # 列表处理
            return [cls.data_to_model(item, to_model=to_model) for item in data_obj]

        else:
            raise ValueError(f"不支持此{data_obj}类型的序列化转换")

    @classmethod
    def model_to_data(
        cls,
        model_obj: Union[
            BaseModel,
            BaseOrmTable,
            dataclass,
            List[BaseModel],
            List[BaseOrmTable],
            List[dataclass],
        ],
    ) -> Union[dict, List[dict], None]:
        """
        将 Pydantic 模型或 SQLAlchemy 模型对象转换回原始字典或列表对象。

        Args:
            model_obj: 支持 Pydantic 模型对象、SQLAlchemy 模型、dataclass 对象，或者它们的列表

        Notes:
            - 对于实现了 to_dict() 方法的模型对象，将调用该方法返回字典。

        Returns:
            转换后的字典或列表
        """

        if isinstance(model_obj, dict):
            return model_obj

        if isinstance(model_obj, RowMapping):
            return dict(model_obj)

        elif isinstance(model_obj, BaseModel):
            # Pydantic 模型对象处理，model_dump() 返回字典
            return model_obj.model_dump()

        elif isinstance(model_obj, BaseOrmTable):
            # SQLAlchemy 模型对象处理，to_dict() 返回字典
            return model_obj.to_dict()

        elif dataclasses.is_dataclass(model_obj):
            # dataclass 模型对象处理, asdict() 返回字典
            return asdict(model_obj)

        elif hasattr(model_obj, "to_dict"):
            # 如果模型对象有 to_dict 方法，调用该方法返回字典
            return model_obj.to_dict()

        elif isinstance(model_obj, list):
            # 列表处理，递归转换每个元素
            return [cls.model_to_data(item) for item in model_obj]

        else:
            raise ValueError(f"不支持此{model_obj}类型的反序列化转换")
