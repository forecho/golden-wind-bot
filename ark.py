# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import db
import telegram


def trades():
    """
    docstring
    """
    for item in ['ARKK']:
        # for item in ['ARKK', 'ARKQ', 'ARKW', 'ARKG', 'ARKF']:
        data = trade(item)
        t = before_send(data)
        telegram.send_message(t)
        print(t)


def trade(symbol):
    """
    docstring
    """
    headers = {'Content-Type': 'application/json'}
    url = 'https://arkfunds.io/api/v1/etf/trades?symbol={}&period=1d'
    print(url)
    r = requests.get(url.format(symbol), headers=headers)
    d = r.json()
    db.create_if_not_exist(r.text, d.get('date_from'))
    return d


def before_send(data):
    """
    docstring
    """
    direction = {
        'Buy': "买入",
        'Sell': "卖出"
    }
    title = '{}基金 {} 仓位变动: '.format(data.get('symbol'), data.get('date_from'))
    texts = []
    for trade in data.get('trades', []):
        text = '{} {} {} 股，占比 {}'.format(
            direction[trade.get('direction')],
            trade.get('ticker'),
            trade.get('shares'),
            trade.get('etf_percent')
        )
        texts.append(text)

    return "<b>{}</b>\n\n{}".format(title, '\n'.join(texts))


if __name__ == "__main__":
    trades()
