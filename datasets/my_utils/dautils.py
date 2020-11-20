"""Data analysis utilities
"""
import os
import logging.config
from logging import NullHandler

import ipdb
import pandas as pd

from datasets.my_utils import dautils as da, genutils as ge

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

logger_data = logging.getLogger('data')
logger_data.addHandler(NullHandler())


class DataExplorer:
    def __init__(self, dataset_package, data_exploration_module):
        self.package = dataset_package
        self._package_name = self.package.__name__
        self._package_path = self.package.__path__[0]
        self._package_version = dataset_package.__version__
        self.module = data_exploration_module
        self._module_file = os.path.basename(self.module.__file__)
        self._module_logger = self.module.logger
        self._module_name = self.module.__name__
        # =============================================
        # Parse command-line arguments and setup config
        # =============================================
        retval = self._parse_cmdl_args()
        self.cfg_filepath = retval['cfg_filepath']
        self.log_filepath = retval['log_filepath']
        self.cfg_dict = retval['cfg_dict']
        # ==============================
        # Logging setup from config file
        # ==============================
        self._setup_log_from_cfg()
        # ---------
        # Load data
        # ---------
        logger.info("Loading data")
        self.datasets = self._load_data()

    def compute_simple_stats(self):
        for data_type, data in self.datasets.items():
            opts = self.cfg_dict['compute_simple_stats']
            compute_stats = opts['for_{}'.format(data_type)]
            if data is not None and compute_stats:
                excluded_cols = opts['excluded_cols']
                da.compute_simple_stats(data, data_type,
                                        excluded_cols=opts['excluded_cols'])

    def head(self):
        for data_type, data in self.datasets.items():
            n_rows = self.cfg_dict['{}_head'.format(data_type)]
            if data is not None and n_rows:
                logger_data.info("First {} rows of {}\n{}\n".format(
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

    def _parse_cmdl_args(self):
        cfg_data = {'cfg_filepath': None, 'log_filepath': None, 'cfg_dict': None}
        parser = ge.setup_argparser(self._package_version)
        args = parser.parse_args()
        cfg_data['cfg_filepath'], cfg_data['log_filepath'] = ge.get_cfg_filepaths(args)
        # Get config dict
        cfg_data['cfg_dict'] = ge.load_cfg_dict(cfg_data['cfg_filepath'])
        return cfg_data

    def _setup_log_from_cfg(self):
        # NOTE: if quiet and verbose are both activated, only quiet will have an effect
        if self.cfg_dict['quiet']:
            # TODO: disable logging completely? even error messages?
            self.module_logger.disabled = True
        else:
            log_dict = ge.load_cfg_dict(self.log_filepath, is_logging=True)
            if self.cfg_dict['verbose']:
                ge.set_logging_level(log_dict)
            logging.config.dictConfig(log_dict)
            self.module_logger = logging.getLogger(
                ge.get_logger_name(self._package_name,
                                   self._module_name,
                                   self._module_file))
        # =============
        # Start logging
        # =============
        logger.info("Running {} v{}".format(self._package_name, self._package_version))
        logger.debug("Package path: {}".format(self._package_path))
        logger.info("Verbose option {}".format(
            "enabled" if self.cfg_dict['verbose'] else "disabled"))


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


def compute_simple_stats(data, name='data', include_strings=False,
                         add_quantile=False, excluded_cols=None):
    first_msg = f"*** Stats for {name} ***"
    logger_data.info("*" * len(first_msg))
    logger_data.info(f"{first_msg}")
    logger_data.info("*" * len(first_msg))
    logger_data.info(f"Shape: {data.shape}")
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
    logger_data.info("")
    for s_name, s_values in stats.items():
        logger_data.info(f"*** {s_name} ***")
        logger_data.info(s_values)
        logger_data.info("")
    if add_quantile:
        quantiles = [0.1, 0.3, 0.5, 0.75, 0.9]
        for q in quantiles:
            logger_data.info(f"Quantile: {q}")
            logger_data.info(data.quantile(q))
            logger_data.info("")
