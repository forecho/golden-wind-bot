# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import telepot
import helper
from telepot.loop import MessageLoop


def handle(msg):
    msg = telepot.glance(msg)
    print(msg)


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


def send_message(text):
    """
    docstring
    """
    bot = get_bot()
    telegram = helper.config('telegram')
    bot.sendMessage(telegram['chat_id'], text, 'MarkdownV2')


if __name__ == "__main__":
    test()
