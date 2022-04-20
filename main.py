#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
import requests
import json
import sqlite3
from hashlib import md5
import telepot
import helper
import os
import telegram


def get_data():
    """
    docstring
    """
    payload = {
        'section_ids': [1156, 1152, 1153, 1154, 1155],
        "important": True
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
                      
                send_dircord(title, description)

                telegram.send_message(t)


def create_item_to_db(entitie):
    """
    docstring
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    text = '{}_{}'.format(
        entitie.get('title'),
        entitie.get('description')
    )
    symbol = str(md5(text.encode("utf-8")).hexdigest()).lower()
    conn = sqlite3.connect("{}/golden_wind.db".format(current_path))
    c = conn.cursor()
    c.execute('SELECT * FROM news WHERE symbol=?', (symbol,))
    date = entitie.get('publish_at')
    if c.fetchone() is None:
        # 优化效率
        c.execute("INSERT INTO news VALUES (?,?)", (symbol, date))
        conn.commit()
        conn.close()
        return entitie
    else:
        return None



def send_dircord(title, desc):
    """
    docstring
    """
    discord_webhook_url = helper.config('discord_webhook_url')
    if discord_webhook_url is None:
        return

    data["embeds"] = [
        {
            "description" : desc,
            "title" : title
        }
    ]
    response = requests.post(discord_webhook_url, json=data)
    print(response.status_code)
    print(response.content)

if __name__ == "__main__":
    data = get_data()
    format_data(data)
