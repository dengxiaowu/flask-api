# !/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Default configurations.
'''

__author__ = '邓小武'

configs = {
    'debug': True,
    'env': 'test',
    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'database': 'test',
        'charset': 'utf8'
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
    },
    'log': {
        'path': 'app.log'
    },
    'domain': 'http://localhost.cn',
    'upload': {
        'path': '/data/webapps/fund/uploads/',
        'ext': [
            'pdf',
            'png',
            'jpg',
            'jpeg',
            'zip',
            'sql',
            'xlsx',
            'csv',
            'doc',
            'docx',
        ]
    }
}
