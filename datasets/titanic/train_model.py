"""TODO
"""
import logging.config
from logging import NullHandler

# import ipdb

from pyutils import genutils as ge, mlutils as ml

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

logger_data = logging.getLogger('data')
logger_data.addHandler(NullHandler())


def main():
    global logger
    bp = ge.ConfigBoilerplate(__file__)
    cfg_dict = bp.get_cfg_dict()
    logger = bp.get_logger()

    # Load data
    data = ml.Datasets(**cfg_dict)

    # Get model
    clf = ml.get_model(**cfg_dict['model'])

    # Train and get preds
    logger.info("Training model")
    logger_data.debug(f"{clf}")
    clf.fit(data.X, data.y)
    score = clf.score(data.X, data.y)
    logger.info(f"Score on train: {score}")
    logger.info("Getting predictions from test data")
    predictions = clf.predict(data.X_test)

    # TODO: save report (e.g. configs and model with params)


if __name__ == '__main__':
    main()
