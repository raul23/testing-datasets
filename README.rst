======
README
======
Each folder in the `datasets`_ directory represents a dataset I am testing.

.. contents:: **Table of contents**
   :depth: 3
   :local:

Datasets
========
Each folder associated to a dataset contains a ``configs`` package and two
modules (``explore_data.py`` and ``train_model.py``):

- ``configs``: consists of two files to setup the whole ML pipeline
  (``config.py``) and the loggers (``logging.py``)
- ``explore_data.py``: does data exploration of the given dataset such as
  computing stats (e.g. mean, quantiles) and generating charts (e.g. bar
  chart and distribution graphs) in order to better understand the dataset
- ``train_model.py``: trains a ML model (e.g. LogisticRegression) as defined
  in the ``config.py`` file

fifa_rankings_kaggle
--------------------
``generate_data.py``: script for generating the small FIFA dataset used for the
Kaggle's course `Data Visualization`_

`:information_source:`

   This was done more as an exercise to apply what I learned in the Kaggle's
   Pandas course since the FIFA dataset can be downloaded directly from the
   course's notebook.

You need to change the following paths in the script:

- ``input_fifa_filepath``: the path to the dataset *FIFA Soccer Rankings
  International Men's Ranking (August 1993 - June 2018)* which can be downloaded
  from `Kaggle`_
- ``output_fifa_flepath``: filepath where the smaller dataset will be saved as a
  CSV file (provide a .csv extension to the file)


.. URLs
.. _Data Visualization: https://www.kaggle.com/learn/data-visualization
.. _Kaggle: https://www.kaggle.com/tadhgfitzgerald/fifa-international-soccer-mens-ranking-1993now

iris
----
`iris`_ is a package for experimenting with the classic `Iris dataset`_ by
applying data analysis and machine learning to the task of classifying flowers
into one of three iris species.

titanic
-------
`titanic`_ is a package for experimenting with the Kaggle's `Titanic dataset`_
by applying data analysis and machine learning to the task of predicting who
will survive and who will die based on the Titanic passenger data.

.. URLs
.. _data_exploration.py: https://github.com/raul23/testing-datasets/blob/main/datasets/titanic/data_exploration.py
.. _datasets: https://github.com/raul23/testing-datasets/tree/main/datasets
.. _iris: https://github.com/raul23/testing-datasets/tree/main/datasets/iris
.. _Iris dataset: https://www.kaggle.com/uciml/iris
.. _titanic: https://github.com/raul23/testing-datasets/tree/main/datasets/titanic
.. _Titanic dataset: https://www.kaggle.com/c/titanic
.. _train_model.py: https://github.com/raul23/testing-datasets/blob/main/datasets/titanic/train_model.py
