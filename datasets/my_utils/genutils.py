"""General utilities
"""
import argparse
import codecs
import importlib
import json
import logging.config
import os
import sys
from collections import OrderedDict
from logging import NullHandler
from runpy import run_path

import ipdb


def get_short_logger_name(name):
    return '.'.join(name.split('.')[-2:])


logger = logging.getLogger(get_short_logger_name(__name__))
logger.addHandler(NullHandler())


class ConfigBoilerplate:

    def __init__(self, module_file):
        self._module_file = os.path.basename(os.path.splitext(module_file)[0])
        self._package_name = os.path.basename(os.getcwd())
        self.package = importlib.import_module('datasets.' + self._package_name)
        self._package_path = self.package.__path__[0]
        self._package_version = self.package.__version__
        self.module = importlib.import_module(
            'datasets.{}.{}'.format(self._package_name, self._module_file))
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

    def get_cfg_dict(self):
        return self.cfg_dict

    def get_logger(self):
        return self.module_logger

    def _parse_cmdl_args(self):
        cfg_data = {'cfg_filepath': None, 'log_filepath': None, 'cfg_dict': None}
        parser = setup_argparser(self._package_version)
        args = parser.parse_args()
        cfg_data['cfg_filepath'], cfg_data['log_filepath'] = get_cfg_filepaths(args)
        # Get config dict
        cfg_data['cfg_dict'] = load_cfg_dict(cfg_data['cfg_filepath'])
        return cfg_data

    def _setup_log_from_cfg(self):
        # NOTE: if quiet and verbose are both activated, only quiet will have an effect
        if self.cfg_dict['quiet']:
            # TODO: disable logging completely? even error messages?
            self.module_logger.disabled = True
        else:
            log_dict = load_cfg_dict(self.log_filepath, is_logging=True)
            if self.cfg_dict['verbose']:
                set_logging_level(log_dict)
            logging.config.dictConfig(log_dict)
            self.module_logger = logging.getLogger(
                get_logger_name(self._package_name,
                                self._module_name,
                                self._module_file))
        # =============
        # Start logging
        # =============
        logger.info("Running {} v{}".format(self._package_name, self._package_version))
        logger.debug("Package path: {}".format(self._package_path))
        logger.info("Verbose option {}".format(
            "enabled" if self.cfg_dict['verbose'] else "disabled"))


def get_cfg_filepaths(args):
    from configs import __path__ as configs_path
    # Get default config filepaths
    default_cfg = os.path.join(configs_path[0], 'config.py')
    default_log = os.path.join(configs_path[0], 'logging.py')

    # Get config filepaths from args (i.e. command-line)
    cmdline_cfg = os.path.abspath(args.cfg_filepath) if args.cfg_filepath else None
    cmdline_log = os.path.abspath(args.log_filepath) if args.log_filepath else None

    # Get config filepaths from command line (if they are defined) or default ones
    cfg_filepath = cmdline_cfg if cmdline_cfg else default_cfg
    log_filepath = cmdline_log if cmdline_log else default_log

    return cfg_filepath, log_filepath


# TODO: module_file must be the filename (not whole filepath)
def get_logger_name(package_name, module_name, module_file):
    if module_name == '__main__' or not module_name.count('.'):
        logger_name = "{}.{}".format(
            package_name,
            os.path.splitext(module_file)[0])
    elif module_name.count('.') > 1:
        logger_name = '.'.join(module_name.split('.')[-2:])
    else:
        logger_name = module_name
    return logger_name


def get_settings(conf, is_logging=False):
    _settings = {}
    if is_logging:
        return conf['logging']
    for opt_name, opt_value in conf.items():
        if not opt_name.startswith('__') and not opt_name.endswith('__'):
            _settings.setdefault(opt_name, opt_value)
    return _settings


def load_cfg_dict(cfg_filepath, is_logging=False):
    _, file_ext = os.path.splitext(cfg_filepath)
    try:
        if file_ext == '.py':
            cfg_dict = run_path(cfg_filepath)
            cfg_dict = get_settings(cfg_dict, is_logging)
        elif file_ext == '.json':
            cfg_dict = load_json(cfg_filepath)
        else:
            # TODO: log error message
            cfg_dict = None
    except FileNotFoundError:
        return None
    else:
        return cfg_dict


def load_json(filepath, encoding='utf8'):
    """Load JSON data from a file on disk.

    If using Python version betwee 3.0 and 3.6 (inclusive), the data is
    returned as :obj:`collections.OrderedDict`. Otherwise, the data is
    returned as :obj:`dict`.

    Parameters
    ----------
    filepath : str
        Path to the JSON file which will be read.
    encoding : str, optional
        Encoding to be used for opening the JSON file in read mode (the default
        value is '*utf8*').

    Returns
    -------
    data : dict or collections.OrderedDict
        Data loaded from the JSON file.

    Raises
    ------
    OSError
        Raised if any I/O related error occurs while reading the file, e.g. the
        file doesn't exist.

    References
    ----------
    `Are dictionaries ordered in Python 3.6+? (stackoverflow)`_

    """
    try:
        with codecs.open(filepath, 'r', encoding) as f:
            if sys.version_info.major == 3 and sys.version_info.minor <= 6:
                data = json.load(f, object_pairs_hook=OrderedDict)
            else:
                data = json.load(f)
    except OSError:
        raise
    else:
        return data


def set_logging_level(log_dict):
    keys = ['handlers', 'loggers']
    for k in keys:
        for name, val in log_dict[k].items():
            val['level'] = "DEBUG"


def setup_argparser(package_version):
    """Setup the argument parser for the command-line script.

    TODO

    Returns
    -------
    parser : argparse.ArgumentParser
        Argument parser.

    """
    # Setup the parser
    parser = argparse.ArgumentParser(
        # usage="%(prog)s [OPTIONS]",
        # prog=os.path.basename(__file__),
        description='''\
TODO\n
IMPORTANT: these are only some of the most important options. Open the settings 
file to have access to the complete list of options''',
        # formatter_class=argparse.RawDescriptionHelpFormatter)
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # ===============
    # General options
    # ===============
    parser.add_argument("--version", action='version',
                        version='%(prog)s {}'.format(package_version))
    parser.add_argument(
        "-c", "--cfg-filepath", dest="cfg_filepath",
        help='''Filepath to the main configuration file (.py)''')
    parser.add_argument(
        "-l", "--log-filepath", dest="log_filepath",
        help='''Filepath to the logging configuration file (.py)''')
    return parser
