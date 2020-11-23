"""TODO
"""
import logging.config
from logging import NullHandler

from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())


def main():
    global logger

    # Load the data



if __name__ == '__main__':
    main()
