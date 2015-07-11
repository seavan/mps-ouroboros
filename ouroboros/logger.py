# encoding: utf-8

import eventlet
from eventlet.green import thread, threading

import logging

logging.thread = eventlet.green.thread
logging.threading = eventlet.green.threading
logging._lock = logging.threading.RLock()

FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'

logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d_%H:%M:%S', level=logging.INFO)
logger = logging.getLogger('ouroboros')

logging.getLogger("requests").setLevel(logging.WARNING)

def info(msg):
    logger.info(msg)

def error(msg):
    logger.error(msg)

def warn(msg):
    logger.warning(msg)
