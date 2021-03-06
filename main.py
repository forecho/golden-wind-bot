#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
                t = """
                <b>{}</b>

{}""".format(entitie.get('title', '').strip(), entitie.get('description', '').strip())
                # if entitie.get('source_url'):
                #     t = '{}（<a href="{}">来源</a>）'.format(
                #         t, entitie.get('source_url')
                #     )
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


if __name__ == "__main__":
    data = get_data()
    format_data(data)
