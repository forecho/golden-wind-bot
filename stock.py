#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import helper
import telegram
import sys


def get_price(symbol):
    """
    docstring
    """
    s = symbol.upper()
    finnhub = helper.config('finnhub')
    url = 'https://finnhub.io/api/v1/quote?symbol={}&token={}'
    r = requests.get(url.format(s, finnhub['token']))
    data = r.json()
    if data.get('o', 0) != 0:
        return ''
    return """<b>{} 最新报价</b>
当日开盘价: {}
当天的高价: {}
当天的低价: {}
此刻价格: {}
上一个收盘价: {}
""".format(s, data.get('o'), data.get('h'), data.get('l'), data.get('c'), data.get('pc'))


if __name__ == "__main__":
    if sys.argv[1]:
        text = get_price(sys.argv[1])
        telegram.send_message(text)
