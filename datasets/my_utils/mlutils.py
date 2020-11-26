"""Machine learning utilities
"""
import logging.config
from logging import NullHandler

# import ipdb
# import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from datasets.my_utils import genutils as ge

pandas = None

logger = logging.getLogger(ge.get_short_logger_name(__name__))
logger.addHandler(NullHandler())


_ENSEMBLE_METHODS = ['AdaBoostClassifier', 'BaggingClassifier',
                     'ExtraTreesClassifier', 'GradientBoostingClassifier',
                     'RandomForestClassifier', 'StackingClassifier',
                     'HistGradientBoostingClassifier']


class Datasets:

    def __init__(self, train_filepath, test_filepath, y_target, features=None,
                 get_dummies=False, *args, **kwargs):
        # ------------------
        # Parameters parsing
        # ------------------
        global pandas
        logger.info("Importing pandas as pd...")
        import pandas
        self.train_filepath = train_filepath
        self.test_filepath = test_filepath
        self.y_target = y_target
        if features:
            logger.debug(f"Using only these features: {features}")
            self.features = features
        else:
            logger.debug("Using all features")
            self.features = None
        self.get_dummies = get_dummies
        # ------------
        # Data loading
        # ------------
        # Load train data
        logger.info("Loading training data")
        self.train_data = pandas.read_csv(train_filepath)
        if not self.features:
            self.features = self.train_data.columns.to_list()
            # Remove target from features
            self.features.remove(self.y_target)
            logger.debug(f"Using all {len(self.features)} features")
        self.y = self.train_data[y_target]
        # Load test data
        logger.info("Loading test data")
        self.test_data = pandas.read_csv(test_filepath)
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
        self.X = pandas.get_dummies(self.X)
        self.X_test = pandas.get_dummies(self.X_test)


def get_ensemble_method(ensemble_type, ensemble_params):
    logger.info(f"Importing ensemble method: {ensemble_type}")
    if ensemble_type == 'AdaBoostClassifier':
        from sklearn.ensemble import AdaBoostClassifier as ens_clf
    elif ensemble_type == 'BaggingClassifier':
        from sklearn.ensemble import BaggingClassifier as ens_clf
    elif ensemble_type == 'ExtraTreesClassifier':
        from sklearn.ensemble import ExtraTreesClassifier as ens_clf
    elif ensemble_type == 'RandomForestClassifier':
        from sklearn.ensemble import RandomForestClassifier as ens_clf
    elif ensemble_type == 'StackingClassifier':
        from sklearn.ensemble import StackingClassifier as ens_clf
    else:
        raise TypeError(f"Ensemble method not recognized: "
                        f"{ensemble_type}")
    logger.debug(f"Ensemble method imported: {ens_clf}")
    base_model_cfg = ensemble_params.get('base_estimator')
    if base_model_cfg:
        base_model = get_base_model(**base_model_cfg)
        return ens_clf(base_model, **ensemble_params)
    else:
        return ens_clf(**ensemble_params)


def get_base_model(model_type, model_params):
    logger.info(f"Importing {model_type}...")
    if model_type == 'DecisionTreeClassifier':
        from sklearn.tree import DecisionTreeClassifier as clf
    elif model_type == 'ExtraTreeClassifier':
        from sklearn.tree import ExtraTreeClassifier as clf
    elif model_type == 'LinearSVC':
        from sklearn.svm import LinearSVC as clf
    elif model_type == 'LogisticRegression':
        from sklearn.linear_model import LogisticRegression as clf
    elif model_type == 'NuSVC':
        from sklearn.svm import NuSVC as clf
    elif model_type == 'Perceptron':
        # Perceptron() is equivalent to SGDClassifier(loss="perceptron", eta0=1,
        # learning_rate="constant", penalty=None).
        # Ref.: https://bit.ly/3pPnZDc (sklearn-perceptron)
        from sklearn.linear_model import Perceptron as clf
    elif model_type == 'SGDClassifier':
        from sklearn.linear_model import SGDClassifier as clf
    elif model_type == 'SVC':
        from sklearn.svm import SVC as clf
    else:
        raise TypeError(f"Model type not recognized: {model_type}")
    logger.debug(f"Model imported: {clf}")
    return clf(**model_params)


# TODO: catch error in models
def get_clf(model_type, model_params, scale_input=False):
    logger.debug(f"Get model: {model_type}")
    if model_type in _ENSEMBLE_METHODS:
        clf = get_ensemble_method(model_type, model_params)
    else:
        clf = get_base_model(model_type, model_params)
    if scale_input:
        logger.info("Input will be scaled")
        """
        logger.info("Importing sklearn.pipeline.make_pipeline")
        from sklearn.pipeline import make_pipeline
        """
        return make_pipeline(StandardScaler(), clf)
    else:
        return clf
