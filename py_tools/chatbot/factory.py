#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 机器人工厂模块 }
# @Date: 2023/02/19 20:03
from enum import Enum
from typing import Dict, Type
from py_tools.chatbot import DingTalkChatBot, FeiShuChatBot, WeComChatbot, BaseChatBot


class ChatBotType(Enum):
    """群聊机器人类型枚举"""

    FEISHU_CHATBOT = "feishu"
    DINGTALK_CHATBOT = "dingtalk"
    WECOM_CHATBOT = "wecom"


class ChatBotFactory(object):
    """
    消息机器人工厂
    支持 飞书、钉钉、自定义机器人消息发送
    """

    # 群聊机器人处理类映射
    CHATBOT_HANDLER_CLS_MAPPING: Dict[ChatBotType, Type[BaseChatBot]] = {
        ChatBotType.FEISHU_ROBOT.value: FeiShuChatBot,
        ChatBotType.DINGTALK_ROBOT.value: DingTalkChatBot,
        ChatBotType.WECOM_CHATBOT.value: WeComChatbot
    }

    def __init__(self, chatbot_type: ChatBotType):
        if chatbot_type not in self.CHATBOT_HANDLER_CLS_MAPPING:
            raise ValueError(f"不支持 {chatbot_type} 类型的机器人")
        self.robot_type = chatbot_type

    def build(self, webhook_url: str, secret: str = None) -> BaseChatBot:
        """
        构造具体的机器人处理类
        Args:
            webhook_url: 机器人webhook地址
            secret: 机器人密钥

        Returns: 根据 robot_type 返回对应的机器人处理类

        """
        chatbot_handle_cls = self.CHATBOT_HANDLER_CLS_MAPPING.get(self.robot_type)
        return chatbot_handle_cls(webhook_url=webhook_url, secret=secret)


def main():
    feishu_webhook = "xxx"
    feishu_webhook_secret = "xxx"

    dingtalk_webhook = "xxx"
    dingtalk_webhook_secret = "xxx"

    feishu_chatbot = ChatBotFactory(chatbot_type=ChatBotType.FEISHU_CHATBOT.value).build(
        webhook_url=feishu_webhook,
        secret=feishu_webhook_secret
    )
    content = "飞书自定义机器人使用指南：\n https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN"
    feishu_chatbot.send_msg(content)

    dingtalk_chatbot = ChatBotFactory(chatbot_type=ChatBotType.DINGTALK_CHATBOT.value).build(
        webhook_url=dingtalk_webhook,
        secret=dingtalk_webhook_secret
    )
    content = "钉钉自定义机器人使用指南：\n https://open.dingtalk.com/document/robots/custom-robot-access"
    dingtalk_chatbot.send_msg(content)


if __name__ == '__main__':
    main()
