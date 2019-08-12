#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @time  : 2019/7/3  下午2:24
import logging

log = logging.getLogger(__name__)


dev = {
    'run_info': {
        'host': '0.0.0.0',
        'debug': True,
        'port': 5000,
        'workers': 4,

        # host=None,
        # port=None,
        # debug=False,
        # ssl=None,
        # sock=None,
        # workers=1,
        # protocol=None,
        # backlog=100,
        # stop_event=None,
        # register_sys_signals=True,
        # access_log=True,
    },
    'DATABASES': {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",
                "port": "3306",
                "user": "root",
                "password": "123456",
                "database": "api"
            }
        }
    },
    "LOG_SETTINGS": {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'filters': ['requestid'],
            },
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s %(name)s:%(lineno)d %(request_id)s | %(message)s',
            },
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': True
            },
        }
    }
}
prod = {
    'run_info': {
        'host': '0.0.0.0',
        'port': 5000,
        'workers': 4
    },
    'DATABASES': {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",
                "port": "3306",
                "user": "root",
                "password": "123456",
                "database": "apeland"
            },
            'OPTIONS': {
                "init_command": "SET foreign_key_checks = 0;",
            }
        }
    }
}
