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
from message.slack import Slack
from message.telegram import Telegram


def get_data():
    """
    docstring
    """
    payload = {
        'section_ids': [1156, 1152, 1153, 1154, 1155],
        "important": 1
    }
    url = 'https://m.lbkrs.com/api/forward/v2/news/sections'
    r = requests.post(url, data=payload)
    # return json.dumps(r.json(), encoding="utf-8", ensure_ascii=False)
    return r.json()


def format_data(data):
    """
    docstring
    """
    sections = data.get('data').get('sections', [])
    for section in sections:
        entities = section.get('entities', [])
        for entitie in entities:
            if create_item_to_db(entitie) is not None:
                description =  entitie.get('description', '').strip()
                title = entitie.get('title', '').strip()
                t = """
                <b>{}</b>

{}""".format(title, description)
                # if entitie.get('source_url'):
                #     t = '{}（<a href="{}">来源</a>）'.format(
                #         t, entitie.get('source_url')
                #     )
                      
                Discord.send_message(title, description)
                Slack.send_message(title, description)
                Telegram.send_message(t)


def create_item_to_db(entitie):
    """
    docstring
    """
    text = '{}_{}'.format(
        entitie.get('title'),
        entitie.get('description')
    )
    date = entitie.get('publish_at')
    if db.create_if_not_exist(text, date):
        return entitie
    else:
        return None

if __name__ == "__main__":
    data = get_data()
    format_data(data)
