"""Data analysis utilities
"""
import logging.config
from logging import NullHandler

import ipdb

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def remove_columns(data, excluded_cols):
    cols = set(data.columns)
    valid_cols = cols - set(excluded_cols)
    if excluded_cols:
        logger.info(f"Excluded columns: {cols.intersection(excluded_cols)}")
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
        logger.info(f"Rejected strings columns: {strings_cols}")
        return data[num_cols]
    else:
        logger.info("No strings columns found in the data")
        return data


def compute_simple_stats(data, name='data', include_strings=False, add_quantile=False, excluded_cols=None):
    first_msg = f"*** Stats for {name} ***"
    logger.info("*" * len(first_msg))
    logger.info(f"{first_msg}")
    logger.info("*" * len(first_msg))
    if excluded_cols:
        data = remove_columns(data, excluded_cols)
    if not include_strings:
        data = remove_strings_from_cols(data)
    stats = {
        'mean': data.mean(),
        'median': data.median(),
        'std': data.std(),
        'max': data.max(),
        'min': data.min()
    }
    logger.info("")
    for s_name, s_values in stats.items():
        logger.info(f"*** {s_name} ***")
        logger.info(s_values)
        logger.info("")
    if add_quantile:
        quantiles = [0.1, 0.3, 0.5, 0.75, 0.9]
        for q in quantiles:
            logger.info(f"Quantile: {q}")
            logger.info(data.quantile(q))
            logger.info("")
