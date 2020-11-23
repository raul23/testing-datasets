"""TODO
"""
import logging.config
from logging import NullHandler

import ipdb

from datasets.my_utils import genutils as ge, mlutils as ml

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def main():
    global logger
    bp = ge.ConfigBoilerplate(__file__)
    cfg_dict = bp.get_cfg_dict()
    logger = bp.get_logger()

    # Load data
    data = ml.Datasets(**cfg_dict)

    # Get model
    logger.debug(f"Get model: {cfg_dict['model']['model_type']}")
    clf = ml.get_model(**cfg_dict['model'])

    # Train and get preds
    logger.info("Train model")
    clf.fit(data.X, data.y)
    score = clf.score(data.X, data.y)
    logger.info(f"Score on train: {score}")
    logger.info("Get predictions from test data")
    predictions = clf.predict(data.X_test)


if __name__ == '__main__':
    main()
