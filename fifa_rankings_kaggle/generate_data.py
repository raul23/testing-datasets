"""Generate the Fifa dataset used for the Kaggle's course Data Visualization

We start from the dataset FIFA Soccer Rankings International Men's Ranking
(August 1993 - June 2018) which can be downloaded from
https://www.kaggle.com/tadhgfitzgerald/fifa-international-soccer-mens-ranking-1993now

Sample of the dataset:
            rank country_full country_abrv  total_points  ...
rank_date                                                 ...
1993-08-08     1      Germany          GER           0.0
1993-08-08     2        Italy          ITA           0.0  ...
1993-08-08     3  Switzerland          SUI           0.0  ...
1993-08-08     4       Sweden          SWE           0.0  ...


We transform it in order to get the rankings for only 6 countries as in the
Kaggle course: ARG, BRA, ESP, FRA, GER, ITA

End result of the smaller dataset that will be generated (first 5 rows):

            ARG	   BRA	 ESP	FRA	   GER	  ITA
Date
1993-08-08	5.0	   8.0	 13.0       12.0           1.0	  2.0
1993-09-23	12.0           1.0	 14.0       7.0	   5.0	  2.0
1993-10-22	9.0	   1.0	 7.0	14.0           4.0	  3.0
1993-11-19	9.0	   4.0	 7.0	15.0           3.0	  1.0
1993-12-23	8.0	   3.0	 5.0	15.0           1.0	  2.0
....

"""
import os

import ipdb
import pandas as pd

# We start with this dataset of FIFA rankings:
input_fifa_filepath = os.path.expanduser('~/Data/kaggle_datasets/fifa_rankings/fifa_ranking.csv')
# Filepath where the smaller dataset will be saved
output_fifa_flepath = os.path.expanduser('~/Data/kaggle_datasets/fifa_kaggle_course/fifa.csv')


def main():
    # Load the FIFA rankings dataset
    fifa_data = pd.read_csv(input_fifa_filepath, index_col="rank_date", parse_dates=True)
    # Change index name rank_date to Date
    fifa_data = fifa_data.rename_axis("Date", axis='rows')
    # Change the column rank's type from int64 to float64
    # IMPORTANT: don't use column names associated with built-in pandas
    # properties such as rank.
    # Can't use fifa_data.rank to access this column since it is a pandas method
    fifa_data['rank'] = fifa_data['rank'].astype('float64')
    # Only take rows associated with the following countries: ARG, BRA, ESP,
    # FRA, GER, ITA
    countries = ['ARG', 'BRA', 'ESP', 'FRA', 'GER', 'ITA']
    fifa_data = fifa_data[fifa_data.country_abrv.isin(countries)]
    # Only take the following two columns: rank and country_abrv
    fifa_data = fifa_data.loc[:, ['rank', 'country_abrv']]
    # Sort by date and country. Hence the countries will be in the correct
    # order we want
    fifa_data = fifa_data.sort_values(['Date', 'country_abrv'])
    # Get unique values of dates which will be used as the indexes in our
    # smaller FIFA dataset of 6 countries
    dates = fifa_data.index.unique()
    # At this moment, the FIFA dataset has the following structure:
    #
    # index: Date
    # columns: rank, country_abrv
    # Example of row: 1993-08-08  5.0  ARG

    # However, what we want is the following structure:
    #
    # index: Date (must be unique dates)
    # columns: ARG BRA ESP FRA GER ITA
    # Example of row: 1993-08-08  5.0  8.0  13.0  12.0  1.0  2.0

    # Dictionary of countries (abr) and theirs rankings across the years
    country_rankings = {}

    def get_country_rankings(row):
        country_rankings.setdefault(row['country_abrv'], [])
        country_rankings[row['country_abrv']].append(row['rank'])

    # Build a dictionary of countries and their rankings which will be used to
    # build a DataFrame
    fifa_data.apply(get_country_rankings, axis='columns')
    fifa_data = pd.DataFrame(country_rankings)
    # Change the index (row numbers from 0 to 285) to Dates (unique values)
    fifa_data = fifa_data.set_index(dates)
    # Save the dataset as CSV
    fifa_data.to_csv(output_fifa_flepath)


if __name__ == '__main__':
    main()
