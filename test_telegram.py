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


telegram = helper.helper.config('telegram')
bot = telepot.Bot(telegram['token'])
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
