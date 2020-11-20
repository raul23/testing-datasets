"""TODO
"""
import logging.config
import os
from logging import NullHandler

import ipdb
import pandas as pd

from configs import __path__ as configs_path
from datasets.my_utils import dautils as da, genutils as ge
from datasets.titanic import (__name__ as package_name,
                              __path__ as package_path,
                              __version__ as package_version)

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def main():
    ipdb.set_trace()
    ge.setup_argparser(package_version)


if __name__ == '__main__':
    main()
