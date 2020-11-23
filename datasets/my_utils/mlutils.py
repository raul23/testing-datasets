"""Machine learning utilities
"""
import logging.config
from logging import NullHandler

import ipdb
import pandas as pd

from datasets.my_utils import genutils as ge

logger = logging.getLogger(ge.get_short_logger_name(__name__))
logger.addHandler(NullHandler())


class Datasets:

    def __init__(self, train_filepath, test_filepath, y_target, features=None,
                 get_dummies=False, *args, **kwargs):
        # ------------------
        # Parameters parsing
        # ------------------
        self.train_filepath = train_filepath
        self.test_filepath = test_filepath
        self.y_target = y_target
        if features:
            logger.debug(f"Using these features: {features}")
            self.features = features
        else:
            logger.debug("Using all features")
            self.features = []
        self.get_dummies = get_dummies
        # ------------
        # Data loading
        # ------------
        # Load train data
        logger.info("Loading training data")
        self.train_data = pd.read_csv(train_filepath)
        self.y = self.train_data[y_target]
        # Load test data
        logger.info("Loading test data")
        self.test_data = pd.read_csv(test_filepath)
        # ------------------
        # Data preprocessing
        # ------------------
        # Select only the required features
        # TODO: remove target from train X
        self.X = self.train_data[self.features]
        self.X_test = self.test_data[self.features]
        if self.get_dummies:
            self._get_dummies()

    # One-hot encode the data
    def _get_dummies(self):
        # Replace missing values on train and test
        logger.info("One-hot encoding the data")
        self.X = pd.get_dummies(self.X)
        self.X_test = pd.get_dummies(self.X_test)


# TODO: catch error in models
def get_model(model_type, model_params, *args, **kwargs):
    logger.debug(f"Get model: {model_type}")
    logger.info(f"Importing {model_type}...")
    if model_type == 'LogisticRegression':
        from sklearn.linear_model import LogisticRegression as model
    elif model_type == 'RandomForestClassifier':
        from sklearn.ensemble import RandomForestClassifier as model
    else:
        raise TypeError(f"Model type not supported: {model_type}")
    return model(**model_params)




