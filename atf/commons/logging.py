#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import colorlog

logger = None

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


def log_init(report):
    global logger

    log_file_path = report
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    log_file_path = os.path.join(log_file_path,"project.log")

    logger = logging.getLogger(logging.NOTSET)
    logger.setLevel(logging.NOTSET)

    formatter = logging.Formatter('%(asctime)s %(levelname)s :%(message)s')

    formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
        log_colors=log_colors_config)  # 日志输出格式


    ch = logging.StreamHandler(stream=sys.stdout)
    rh = logging.handlers.RotatingFileHandler(log_file_path, mode='a', maxBytes=50 * 1024 * 1024, backupCount=10)

    logger.addHandler(ch)
    logger.addHandler(rh)

    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)

    rh.setFormatter(formatter)
    rh.setLevel(logging.INFO)
    logger.info('init...')

def log_info(message):
    try:
        logger.info(message)
    except:
        print(message)


def log_warning(message):
    try:
        logger.warning(message)
    except:
        print(message)


def log_error(message,exit=True):
    try:
        logger.error(message)
        if exit:
            os._exit(0)
    except:
        print(message)

