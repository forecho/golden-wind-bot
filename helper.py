# !/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import os
import random


class helper:
    def __init__(self):
        pass

    @staticmethod
    def config(key):
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open("{}/config.yml".format(current_path), 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        try:
            value = cfg[key]
        except Exception:
            return ''
        return value

    @staticmethod
    def get_ua():
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open("{}/newUa.txt".format(current_path), 'r') as fileua:
            uas = fileua.readlines()
            cnt = random.randint(0, len(uas)-1)
            return uas[cnt].replace("\n", "")

    @staticmethod
    def get_header(referer):
        header = {
            'Referer': referer,
            'User-agent': helper.get_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accetp-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
        }
        return header


if __name__ == '__main__':
    helper()
