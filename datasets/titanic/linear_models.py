"""TODO
"""
import logging.config
from logging import NullHandler

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def main():
    global logger


if __name__ == '__main__':
    main()
