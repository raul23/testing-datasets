======
README
======
Each folder in the directory ``datasets/`` (except ``my_utils``) represents a different dataset I am testing (e.g. data exploration, applying ML). Here is a desription of each of them.

my_utils
========

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

titanic
=======

