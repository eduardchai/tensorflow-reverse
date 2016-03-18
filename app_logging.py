# From https://github.com/salestock/abtest/blob/develop/app_logging.py
import os
import logging
import socket
from logging.handlers import SysLogHandler

class ContextFilter(logging.Filter):

      hostname = socket.gethostname()

      def filter(self, record):
          record.hostname = ContextFilter.hostname
          return True

def get_syslog_handler():
    papertrail_port = os.environ.get('SS_SORAYA_RECO_LOGGING_PORT')
    papertrail_host= 'logs4.papertrailapp.com'

    if not papertrail_port:
        return None

    syslog = SysLogHandler(address=(papertrail_host, int(papertrail_port)))
    formatter = logging.Formatter('%(asctime)s [%(process)d] %(name)s : %(message)s', datefmt='%b %d %H:%M:%S')

    syslog.setLevel(logging.DEBUG)
    syslog.setFormatter(formatter)

    return syslog

def get_default_handler():
    handler = logging.FileHandler('soraya_recommender.log')
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(process)d] %(name)s : %(levelname)s : %(message)s')
    handler.setFormatter(formatter)

    return handler

def get_logger():

    logger = logging.getLogger('soraya_recommender')
    logger.setLevel(logging.INFO)

    f = ContextFilter()
    logger.addFilter(f)

    syslog_handler = get_syslog_handler()

    if syslog_handler:
        logger.addHandler(syslog_handler)
    else:
        logger.addHandler(get_default_handler())

    return logger
