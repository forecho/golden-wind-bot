#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import sqlite3
from hashlib import md5
import helper
import db
import os

from message.discord import Discord
from message.slack import slack
from message.telegram import Telegram

# 添加这一行来确保表存在
db.create_table_if_not_exists()

# 添加这一行来初始化 Telegram
telegram = Telegram()

def get_data():
    """
    获取数据
    """
    payload = {
        'page': 1,
        'page_size': 20,  # 可以根据需要调整
        "score": 0
    }
    url = 'https://api.chaomeigu.com/v1/news/latest'  # 移除了查询参数
    try:
        r = requests.get(url, params=payload)  # 使用 GET 请求和 params 参数
        r.raise_for_status()  # 检查请求是否成功
        return r.json()
    except requests.RequestException as e:
        print(f"请求错误：{e}")
        print(f"响应内容：{r.text}")  # 打印响应内容以便调试
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 解码错误：{e}")
        print(f"响应内容：{r.text}")  # 打印响应内容以便调试
        return None

def format_data(data):
    """
    格式化数据
    """
    items = data.get('data', {}).get('items', [])
    for item in items:
        if create_item_to_db(item) is not None:
            title = item.get('title', '').strip()
            content = item.get('content', '').strip()
            t = """
            <b>{}</b>

{}""".format(title, content)
            Discord.send_message(title, content)
            
            # Slack 消息发送
            if slack and slack.client:
                print("尝试发送 Slack 消息")
                slack.send_message(title, content)
            else:
                print("Slack 未配置或客户端未初始化，跳过发送")
            
            # Telegram 消息发送
            try:
                print("正在尝试发送 Telegram 消息")
                telegram.send_message(t)
                print("Telegram 消息发送成功")
            except Exception as e:
                print(f"发送 Telegram 消息时出错：{str(e)}")

def create_item_to_db(item):
    """
    创建数据库项目
    """
    text = '{}_{}'.format(
        item.get('title'),
        item.get('content')
    )
    date = item.get('created_at')
    if db.create_if_not_exist(text, date):
        return item
    else:
        return None

if __name__ == "__main__":
    # 添加调试信息
    print(f"Slack 配置状态：{'已配置' if slack and slack.client else '未配置'}")
    
    data = get_data()
    if data:
        format_data(data)
    else:
        print("无法获取数据，请检查网络连接或 API 状态。")
