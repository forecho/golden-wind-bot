# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import helper

def send_message(title, desc):
    """
    docstring
    """
    discord_webhook_url = helper.config('discord_webhook_url')
    if discord_webhook_url is None:
        return
    data = []
    data["embeds"] = [
        {
            "description" : desc,
            "title" : title
        }
    ]
    response = requests.post(discord_webhook_url, json=data)
    print(response.status_code)
    print(response.content)

