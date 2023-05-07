#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 机器人应用服务模块 }
# @Date: 2023/05/03 18:51
import json
from typing import List

import requests
from cacheout import Cache
from loguru import logger

from py_tools.enums.feishu import FeishuReceiveType
from py_tools.exceptions import SendMsgException


class FeiShuAppServer:
    """飞书应用服务类"""

    # 用于缓存应用的access_token，减少http请求
    token_cache = Cache()

    # 通过飞书应用的 app_id, app_secret 获取 access_token
    # API参考: https://open.feishu.cn/document/ukTMukTMukTM/uMTNz4yM1MjLzUzM
    GET_FEISHU_TENANT_ACCESS_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

    # 获取飞书用户 open_id
    # API参考: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/batch_get_id
    GET_FEISHU_USER_OPEN_ID_URL = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id"

    # 给飞书用户/群聊发送消息
    # API参考: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
    NOTIFY_FEISHU_USER_MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"

    # 获取用户或机器人所在的群列表
    # API参考: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat/list
    GET_FEISHU_USER_OF_GROUP_URL = "https://open.feishu.cn/open-apis/im/v1/chats"

    def __init__(self, app_id: str, app_secret: str, timeout=10):
        """
        飞书应用服务初始化
        Args:
            app_id: 应用id
            app_secret: 应用密钥
            timeout: 请求连接超时 默认10s
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.token_cache_key = f"{app_id}:{app_secret}:token"  # 用于缓存 access_token 的key
        self.req_timeout = timeout

    def _get_tenant_access_token(self):
        """
        获取飞书access_token用于访问飞书相关接口
        先从程序缓存中获取，没有则再发请求获取
        API参考: https://open.feishu.cn/document/ukTMukTMukTM/uMTNz4yM1MjLzUzM
        """

        # 先从程序内存缓存中获取 tenant_access_token
        tenant_access_token = self.token_cache.get(key=self.token_cache_key)
        if tenant_access_token:
            logger.debug(f"cache get tenant_access_token {tenant_access_token}")
            return tenant_access_token

        # 缓存没有再请求
        app_info = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url=self.GET_FEISHU_TENANT_ACCESS_TOKEN_URL, json=app_info, timeout=self.req_timeout)
        ret_info = resp.json()
        if ret_info.get("code") != 0:
            raise ValueError(f"FeiShuAppServer get_tenant_access_token error, {ret_info}")

        expire = ret_info.get("expire", 0)
        tenant_access_token = ret_info.get("tenant_access_token")
        ttl = expire - 5 * 60  # 缓存比过期时间少5分钟

        # 存入当前程序内存中过期则才重新访问请求获取
        self.token_cache.set(key=self.token_cache_key, value=tenant_access_token, ttl=ttl)

        return tenant_access_token

    def _get_user_open_id(
            self,
            mobiles: list = None,
            emails: list = None,
            user_id_type: FeishuReceiveType = FeishuReceiveType.OPEN_ID
    ) -> List[dict]:
        """
        根据手机号或邮箱号获取飞书用户的open_id
        API参考: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/batch_get_id

        Args:
            mobiles: 飞书用户手机号列表
            emails:  飞书用户邮箱列表
            user_id_type: 用户 ID 类型，默认 open_id

        Raises:
            ValueError

        Returns: user_list
            [
                {"mobile": "130xxxx1752", "user_id": "ou_xxx"},
                {"email": "liuminhui@fuzhi.ai", "user_id": "ou_xxx"}
            ]
        """
        if not mobiles and not emails:
            raise ValueError("FeiShuAppServer _get_user_open_id error, 手机号或邮箱需必填一项")

        receiver_info = {
            "mobiles": mobiles,
            "emails": emails
        }

        headers = {"Authorization": f"Bearer {self._get_tenant_access_token()}"}
        resp = requests.post(
            url=self.GET_FEISHU_USER_OPEN_ID_URL,
            params={"user_id_type": user_id_type.value},
            json=receiver_info,
            headers=headers,
            timeout=self.req_timeout
        )
        ret_info = resp.json()
        if ret_info.get("code") != 0:
            raise ValueError(
                f"FeiShuAppServer _get_user_open_id error, mobiles is {mobiles}, emails is {emails}, {ret_info}"
            )

        user_list = ret_info.get("data", {}).get("user_list")
        return user_list

    def _get_user_or_bot_groups(self, user_id_type: str = FeishuReceiveType.OPEN_ID.value, page_size: int = 100):
        """
        获取用户或机器人所在的群列表
        参考API: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat/list

        Args:
            user_id_type: 用户id类型，默认 open_id
            page_size: 分页大小，默认每次拉取100

        Raises:
            ValueError

        Returns: all_groups
        """

        all_groups = list()  # 收集所有的群聊列表信息
        has_more = True  # 是否有更多的数据
        while has_more:
            # 循环分页获取所有的群聊
            headers = {"Authorization": f"Bearer {self._get_tenant_access_token()}"}
            query_params = {
                "user_id_type": user_id_type,
                "page_size": page_size,
            }
            resp = requests.get(
                url=self.GET_FEISHU_USER_OF_GROUP_URL,
                params=query_params,
                headers=headers,
                timeout=self.req_timeout
            )
            ret_info = resp.json()
            if ret_info.get("code") != 0:
                raise ValueError(f"FeiShuAppServer _get_user_chat_id error, {ret_info}")

            group_data = ret_info.get("data", {})
            has_more = group_data.get("has_more")
            page_token = group_data.get("page_token")
            group_items = group_data.get("items", [])
            all_groups.extend(group_items)
            query_params["page_token"] = page_token  # 继续获取分页数据时需要带上page_token

        return all_groups

    def send_msg(self, content: str, receive_id_type: FeishuReceiveType, receive_id: str):
        """
        发送飞书单聊、群聊信息
        API参考: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create

        Args:
            content: 消息内容
            receive_id_type: 消息接收者id类型 open_id/user_id/union_id/email/chat_id
            receive_id: 消息接收者的ID，ID类型应与查询参数 receive_id_type 对应

        Raises:
            SendError

        Returns:
        """
        msg_data = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": json.dumps({"text": content}, ensure_ascii=False)
        }
        headers = {"Authorization": f"Bearer {self._get_tenant_access_token()}"}
        try:
            resp = requests.post(
                url=self.NOTIFY_FEISHU_USER_MSG_URL,
                params={"receive_id_type": receive_id_type.value},
                json=msg_data,
                headers=headers,
                timeout=self.req_timeout
            )
            ret_info = resp.json()
            if ret_info.get("code") != 0:
                raise ValueError(f"FeiShuTaskChatBot user_task_notify error, {ret_info}")
        except Exception as e:
            raise SendMsgException(e) from e


class FeiShuTaskChatBot(FeiShuAppServer):
    """
    飞书任务通知机器人
    支持单聊通知、群聊通知
    """

    def user_task_notify(self, content: str, receive_mobiles: list = None, receive_emails: list = None):
        """
        用户任务单聊通知
        参考API: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        步骤:
            1、通过 app_id、app_secret 换取 access_token
            2、通过 access_token 和 手机号 查询飞书用户 open_id
            3、最后通过 open_id 让机器人通知指定的用户

        Args:
            content: 通知的内容
            receive_mobiles: 用户接受者的飞书手机号列表
            receive_emails: 用户接受者的飞书邮箱号列表

        Returns:
        """
        user_list = self._get_user_open_id(receive_mobiles, receive_emails)
        # 手机号和邮箱是同一用户的open_id会相同，故用set推导式去重
        open_ids = {user_item.get("user_id") for user_item in user_list if user_item.get("user_id")}
        for open_id in open_ids:
            # 给每个用户发送单聊通知
            try:
                self.send_msg(content, receive_id_type=FeishuReceiveType.OPEN_ID, receive_id=open_id)
            except Exception as e:
                logger.error(str(e))
                continue

    def user_group_task_notify(
            self, content: str,
            group_name: str,
            receive_mobiles: list = None,
            receive_emails: list = None
    ):
        """
        用户任务群聊通知
        参考API: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        步骤:
            1、通过 app_id、app_secret 换取 access_token
            2、通过 access_token 和 手机号 查询飞书用户 open_id
            3、通过 群聊名称过滤出 chat_id
            4、最后通过群聊的 chat_id 和 用户的 open_id 通知指定群聊的用户

        Args:
            content: 通知的内容
            group_name: 群聊名称
            receive_mobiles: 用户接受者的飞书手机号列表
            receive_emails: 用户接受者的邮箱列表

        Raises:
            SendError

        Returns:
        """

        # 根据群聊名称获取群聊机器人所在群组的 chat_id
        group_items = self._get_user_or_bot_groups()
        group_dict = {group_info.get("name"): group_info.get("chat_id") for group_info in group_items}
        chat_id = group_dict.get(group_name)
        if not chat_id:
            raise SendMsgException(f"未找到 {group_name} 的群聊")

        at_user_str = ""
        if receive_mobiles or receive_emails:
            # 需要 at 群内用户则通过手机号或邮箱获取用户open_id
            user_list = self._get_user_open_id(receive_mobiles, receive_emails)
            open_ids = {user_item.get("user_id") for user_item in user_list if user_item.get("user_id")}
            at_user_str = "".join([f'<at user_id="{open_id}"></at>' for open_id in open_ids])

        # 发送通知请求
        msg_content = f"{content}\n{at_user_str}"
        self.send_msg(msg_content, receive_id_type=FeishuReceiveType.CHAT_ID, receive_id=chat_id)
