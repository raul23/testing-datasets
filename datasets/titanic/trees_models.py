"""TODO
"""
import logging.config
from logging import NullHandler

import ipdb
# from sklearn.ensemble import RandomForestClassifier

from datasets.my_utils import genutils as ge

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def main():
    global logger
    cfg = ge.ConfigBoilerplate(__file__)
    logger = cfg.get_logger()
    logger.info("test")

    # Load the data


if __name__ == '__main__':
    main()
