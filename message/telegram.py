# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import telepot
import helper
from telepot.loop import MessageLoop

class Telegram:
    @staticmethod
    def get_bot():
        """
        docstring
        """
        telegram = helper.config('telegram')
        return telepot.Bot(telegram['token'])


    @staticmethod
    def send_message(text, parse_mode='HTML'):
        """
        docstring
        """
        bot = Telegram.get_bot()
        telegram = helper.config('telegram')
        bot.sendMessage(telegram['chat_id'], text, parse_mode=parse_mode)
