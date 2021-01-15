#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3


def db():
    """
    docstring
    """
    conn = sqlite3.connect('golden_wind.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE news (symbol text, date text)''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    db()
