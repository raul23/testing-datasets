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

import data_exploration
from datasets import titanic
from datasets.my_utils import dautils as da
logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def main():
    global logger
    data = da.DataExplorer(titanic, data_exploration)
    logger = data.module_logger
    data.compute_simple_stats()
    data.head()


if __name__ == '__main__':
    main()
