"""Data analysis utilities
"""
import logging.config
from logging import NullHandler

import ipdb
import pandas as pd

from datasets.my_utils import genutils as ge

logger = logging.getLogger(ge.get_short_logger_name(__name__))
logger.addHandler(NullHandler())

logger_data = logging.getLogger('data')
logger_data.addHandler(NullHandler())


class DataExplorer:
    def __init__(self, cfg_dict):
        self.cfg_dict = cfg_dict
        # ---------
        # Load data
        # ---------
        logger.info("Loading data")
        self.datasets = self._load_data()

    def compute_stats(self):
        for data_type, data in self.datasets.items():
            opts = self.cfg_dict['compute_stats']
            is_stats = opts['for_{}'.format(data_type)]
            if data is not None and is_stats:
                compute_stats(data, data_type,
                              excluded_cols=opts['excluded_cols'])

    def count_null(self):
        for data_type, data in self.datasets.items():
            isnull = self.cfg_dict['{}_isnull'.format(data_type)]
            if data is not None and isnull:
                logger_data.info(
                    "*** Number of missing values for each feature in {} "
                    "***\n{}\n".format(
                        data_type,
                        data.isnull().sum()))

    def head(self):
        for data_type, data in self.datasets.items():
            n_rows = self.cfg_dict['{}_head'.format(data_type)]
            if data is not None and n_rows:
                logger_data.info("*** First {} rows of {} ***\n{}\n".format(
                    n_rows,
                    data_type,
                    data.head(n_rows)))

    def _load_data(self):
        datasets = {
            'data': None,
            'train': None,
            'valid': None,
            'test': None
        }
        for k, v in datasets.items():
            filepath = self.cfg_dict['{}_filepath'.format(k)]
            if filepath:
                datasets[k] = pd.read_csv(filepath)
            else:
                # TODO: logging (no filepath for dataset)
                pass
        return datasets


def remove_columns(data, excluded_cols):
    cols = set(data.columns)
    valid_cols = cols - set(excluded_cols)
    if excluded_cols:
        logger_data.info(f"Excluded columns: {cols.intersection(excluded_cols)}")
    return data[valid_cols]


def remove_strings_from_cols(data):
    num_cols = []
    strings_cols = []
    for col, dtype in data.dtypes.to_dict().items():
        if dtype.name == 'object':
            strings_cols.append(col)
        else:
            num_cols.append(col)
    if num_cols:
        logger_data.info(f"Rejected strings columns: {strings_cols}")
        return data[num_cols]
    else:
        logger_data.info("No strings columns found in the data")
        return data


def compute_stats(data, name='data', include_strings=False,
                         excluded_cols=None):
    first_msg = f"*** Stats for {name} ***"
    logger_data.info("*" * len(first_msg))
    logger_data.info(f"{first_msg}")
    logger_data.info("*" * len(first_msg))
    logger_data.info(f"Shape: {data.shape}")
    if excluded_cols:
        data = remove_columns(data, excluded_cols)
    if not include_strings:
        data = remove_strings_from_cols(data)
    logger_data.info("")
    logger_data.info(data.describe())
    logger_data.info("")
