# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from hashlib import md5


def conn_db():
    """
    docstring
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect("{}/golden_wind.db".format(current_path))
    return conn


def create_table_if_not_exists():
    """
    创建 news 表（如果不存在）
    """
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS news
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         symbol TEXT UNIQUE,
         date INTEGER)
    ''')
    conn.commit()
    conn.close()


def create_if_not_exist(text, date):
    """
    如果记录不存在，则创建新记录
    """
    create_table_if_not_exists()  # 确保表存在
    
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    symbol = md5(text.encode('utf-8')).hexdigest()
    c.execute('SELECT * FROM news WHERE symbol=?', (symbol,))
    if c.fetchone() is None:
        c.execute('INSERT INTO news (symbol, date) VALUES (?, ?)', (symbol, date))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


def clear():
    """
    docstring
    """
    pass


if __name__ == "__main__":
    clear()
