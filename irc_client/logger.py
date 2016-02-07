""" Logger factory
"""
import logging
ERROR_LOG = 'twitch_irc_error.log'

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler(ERROR_LOG)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
