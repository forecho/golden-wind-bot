# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import telepot
import helper
import stock
import re
from telepot.loop import MessageLoop


def handle(msg):
    content_type, chat_type, chat_id, date, message_id = telepot.glance(
        msg, long=True)
    print(content_type, chat_type, chat_id, date, message_id)
    if content_type == 'text':
        print(msg)
        r = re.match(r'^\$(\w+)', msg['text'])
        if r:
            t = stock.get_price(r.group(1))
            bot = get_bot()
            bot.sendMessage(chat_id, t)


def get_bot():
    """
    docstring
    """
    telegram = helper.config('telegram')
    return telepot.Bot(telegram['token'])


def test():
    """
    docstring
    """
    bot = get_bot()
    MessageLoop(bot, handle).run_as_thread()
    print('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)


def send_message(text, parse_mode='HTML'):
    """
    docstring
    """
    bot = get_bot()
    telegram = helper.config('telegram')
    bot.sendMessage(telegram['chat_id'], text, parse_mode=parse_mode)


if __name__ == "__main__":
    test()
