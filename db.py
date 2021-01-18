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


def create_if_not_exist(text, date):
    """
    docstring
    """
    conn = conn_db()
    c = conn.cursor()
    symbol = str(md5(text.encode("utf-8")).hexdigest()).lower()
    c.execute('SELECT * FROM news WHERE symbol=?', (symbol,))
    if c.fetchone() is None:
        # 优化效率
        c.execute("INSERT INTO news VALUES (?,?)", (symbol, date))
        conn.commit()
        conn.close()
        return True
    else:
        return False


def clear():
    """
    docstring
    """
    pass


if __name__ == "__main__":
    clear()
