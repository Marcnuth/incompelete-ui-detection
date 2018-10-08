#!/usr/bin/python3
# coding=utf-8
import os
from pathlib import Path
import logging
from logging.config import dictConfig

# Constant directory & files
DIR_BASE = Path(os.path.dirname(os.path.realpath(__file__))).parent
RESOURCE_DIR = DIR_BASE / 'resources'
LOGGING_FILE = Path('/tmp/wsdetect.log')

# Logging
dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format"  : "[%(asctime)s] [%(process)d:%(thread)d] [%(levelname)s] [%(name)s] %(filename)s:%(funcName)s:%(lineno)d %(message)s",
            "datefmt" : "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "wsdetect": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOGGING_FILE.absolute().as_posix(),
            "formatter": "basic",
            "encoding": "utf-8",
            "when": "midnight",
            "interval": 1,
            "backupCount": 7
        },
    },
    "loggers": {
        "wsdetect" : {
            "handlers" : ["wsdetect"],
            "propagate": "true",
            "level"    : "INFO"
        }
    }
})

logger = logging.getLogger(__name__)
logger.info('wsdetect logs will be output in dir:%s', LOGGING_FILE.absolute().as_posix())