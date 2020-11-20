======
README
======
Each folder in the `datasets`_ directory (except ``my_utils``) represents a different dataset I am testing (e.g. data exploration, applying machine learning (ML)). Here is a desription for each of them.

`:information_source:`
   
   Each folder associated to a dataset contains a ``configs`` package which defines the configuration files to setup 
   the whole ML pipeline (e.g. data filepaths and models' parameters) and the loggers used throughout the different
   modules:
   
   - ``config.py``: setup the whole ML pipeline
   - ``logging.py``: setup the loggers

.. contents:: **Table of contents**
   :depth: 3
   :local:

my_utils
========
The `my_utils`_ package contains utilities divided into different modules based on their main application. For example,
the `dautils`_ module defines utilities for data analysis such as computing simple statistics (e.g. mean, quantiles) and
generating graphs (e.g. bar chart) on datasets.

fifa_rankings_kaggle
====================
``generate_data.py``: script for generating the small FIFA dataset used for the Kaggle's course `Data Visualization`_

`:information_source:`

   This was done more as an exercise to apply what I learned in the Kaggle's Pandas course since the FIFA dataset can 
   be downloaded directly from the course's notebook.

You need to change the following paths in the file:

- ``input_fifa_filepath``: the path to the dataset *FIFA Soccer Rankings International Men's Ranking (August 1993 - June 2018)* which can be downloaded from `Kaggle`_
- ``output_fifa_flepath``: filepath where the smaller dataset will be saved as a CSV file (provide a .csv extension to the file)


.. URLs
.. _Data Visualization: https://www.kaggle.com/learn/data-visualization
.. _Kaggle: https://www.kaggle.com/tadhgfitzgerald/fifa-international-soccer-mens-ranking-1993now

iris
====

titanic
=======
The `titanic`_ is a package for experimenting with the Kaggle's `Titanic dataset`_
by applying data analysis and machine learning to the task of predicting who
will survive and who will die based on the Titanic passenger data.

The package is divided into a module for doing data exploration (`data_exploration.py`_) and modules defining different
types of ML models.

.. URLs
.. _data_exploration.py: https://github.com/raul23/testing-datasets/blob/main/datasets/titanic/data_exploration.py
.. _datasets: https://github.com/raul23/testing-datasets/tree/main/datasets
.. _dautils: https://github.com/raul23/testing-datasets/blob/main/datasets/my_utils/dautils.py
.. _my_utils: https://github.com/raul23/testing-datasets/tree/main/datasets/my_utils
.. _titanic: https://github.com/raul23/testing-datasets/tree/main/datasets/titanic
.. _Titanic dataset: https://www.kaggle.com/c/titanic
