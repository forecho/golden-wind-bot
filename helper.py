# !/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import os


def config(key):
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open("{}/config.yml".format(current_path), 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    try:
        value = cfg[key]
    except Exception:
        return ''
    return value
