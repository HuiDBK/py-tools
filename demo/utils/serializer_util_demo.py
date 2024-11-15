#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: serializer_util_demo.py
# @Desc: { 序列号工具类 demo }
# @Date: 2024/11/15 17:13
from dataclasses import dataclass

from pydantic import BaseModel
from sqlalchemy import Column, String

from py_tools.connections.db.mysql import BaseOrmTable
from py_tools.utils import SerializerUtil


# sqlalchemy 示例
class UserTable(BaseOrmTable):
    __tablename__ = "user"
    username = Column(String(20))
    email = Column(String(50))


# Pydantic 示例
class UserModel(BaseModel):
    id: int
    username: str
    email: str


@dataclass
class UserDataclass:
    id: int
    username: str
    email: str


class UserCustomModel:
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


def serializer_demo():
    user_table_obj = UserTable(id=2, username="wang", email="wang@example.com")
    user_model_obj = UserModel(id=3, username="zack", email="zack@example.com")
    user_dataclass_obj = UserDataclass(id=4, username="lisa", email="lisa@example.com")
    user_custom_model = UserCustomModel(id=5, username="lily", email="lily@example.com")
    user_infos = [
        {"id": 1, "username": "hui", "email": "hui@example.com"},
        user_table_obj,
        user_model_obj,
        user_dataclass_obj,
        user_custom_model,
    ]

    print("data_to_model")
    user_models = SerializerUtil.data_to_model(data_obj=user_infos, to_model=UserModel)
    print(type(user_models), user_models)

    user_models = SerializerUtil.data_to_model(data_obj=user_infos, to_model=UserTable)
    print(type(user_models), user_models)

    user_models = SerializerUtil.data_to_model(data_obj=user_infos, to_model=UserDataclass)
    print(type(user_models), user_models)

    user_models = SerializerUtil.data_to_model(data_obj=user_infos, to_model=UserCustomModel)
    print(type(user_models), user_models)

    user_model = SerializerUtil.data_to_model(data_obj=user_infos[0], to_model=UserModel)
    user_table = SerializerUtil.data_to_model(data_obj=user_infos[0], to_model=UserTable)
    user_dataclass = SerializerUtil.data_to_model(data_obj=user_infos[0], to_model=UserDataclass)
    print(type(user_model), user_model)
    print(type(user_table), user_table)
    print(type(user_dataclass), user_dataclass)

    # model_to_data
    print("\n\nmodel_to_data")
    user_infos = SerializerUtil.model_to_data(user_infos)
    print(type(user_infos), user_infos)

    user_info = SerializerUtil.model_to_data(user_model_obj)
    print(type(user_info), user_info)

    user_info = SerializerUtil.model_to_data(user_table_obj)
    print(type(user_info), user_info)

    user_info = SerializerUtil.model_to_data(user_dataclass_obj)
    print(type(user_info), user_info)

    user_info = SerializerUtil.model_to_data(user_custom_model)
    print(type(user_info), user_info)


def main():
    serializer_demo()


if __name__ == "__main__":
    main()
