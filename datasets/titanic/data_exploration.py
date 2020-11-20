"""Exploring the Kaggle's Titanic dataset

This module only does data exploration of the Titanic dataset such as computing
simple stats (e.g. mean, quantiles) and generating charts (e.g. bar chart and
distribution graphs) in order to better understand the dataset.

Thus after having explore the dataset under various angles, we can use
machine learning (ML) models to predict who will survive based on the Titanic
passenger data (e.g. name, age, price of ticket, etc).

The ML models are defined in their own modules depending on their types (e.g.
:mod:`linear_models` and :mod:`trees_modules`).

Dataset website: https://www.kaggle.com/c/titanic
"""
import logging.config
from logging import NullHandler

import ipdb
import pandas as pd

from datasets.my_utils import dautils as da, genutils as ge
from datasets.titanic import (__name__ as package_name,
                              __path__ as package_path,
                              __version__ as package_version)

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def main():
    global logger
    # ============================
    # Parse command-line arguments
    # ============================
    parser = ge.setup_argparser(package_version)
    args = parser.parse_args()
    cfg_filepath, log_filepath = ge.get_cfg_filepaths(args)
    # Get config dict
    cfg_dict = ge.load_cfg_dict(cfg_filepath)

    # ==============================
    # Logging setup from config file
    # ==============================
    # NOTE: if quiet and verbose are both activated, only quiet will have an effect
    if cfg_dict['quiet']:
        # TODO: disable logging completely? even error messages?
        logger.disabled = True
    else:
        log_dict = ge.load_cfg_dict(log_filepath, is_logging=True)
        if cfg_dict['verbose']:
            ge.set_logging_level(log_dict)
        logging.config.dictConfig(log_dict)
        logger = logging.getLogger(ge.get_logger_name(__name__, package_name, __file__))

    # =============
    # Start logging
    # =============
    logger.info("Running {} v{}".format(package_name, package_version))
    logger.debug("Package path: {}".format(package_path[0]))
    logger.info("Verbose option {}".format(
        "enabled" if cfg_dict['verbose'] else "disabled"))

    # ---------
    # Load data
    # ---------
    logger.info("Loading data")
    train = pd.read_csv(cfg_dict['train_file_path'])
    test = pd.read_csv(cfg_dict['test_file_path'])

    # --------------------
    # Compute simple stats
    # --------------------
    if cfg_dict['compute_simple_stats']['for_train']:
        da.compute_simple_stats(train, 'train', excluded_cols=['PassengerId'])
    if cfg_dict['compute_simple_stats']['for_test']:
        da.compute_simple_stats(test, 'test', excluded_cols=['PassengerId'])


if __name__ == '__main__':
    main()
