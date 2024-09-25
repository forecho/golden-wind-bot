# !/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Slack:
    def __init__(self):
        # 从配置文件加载
        try:
            # 获取当前文件的目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            current_dir = os.path.dirname(current_dir)
            # 构建配置文件的完整路径
            config_path = os.path.join(current_dir, 'config.yml')
            
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                self.token = config.get('slack_bot_token')
                self.channel = config.get('slack_channel')
        except FileNotFoundError:
            print(f"配置文件 {config_path} 未找到")
            self.token = None
            self.channel = None

        print(f"Slack Bot Token: {'已设置' if self.token else '未设置'}")
        print(f"Slack Channel: {self.channel}")

        if self.token:
            self.client = WebClient(token=self.token)
        else:
            self.client = None
            print("Slack Bot Token 未设置，Slack 功能将被禁用")

    def send_message(self, title, content):
        if not self.client:
            print("Slack 客户端未初始化，无法发送消息")
            return

        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=f"*{title}*\n\n{content}"
            )
            print(f"Slack 消息发送成功：{response['ts']}")
        except SlackApiError as e:
            print(f"Slack 消息发送失败：{e}")
            print(f"错误详情：{e.response['error']}")

slack = Slack()