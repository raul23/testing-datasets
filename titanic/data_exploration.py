import ipdb
import pandas as pd

train_file_path = '~/Data/kaggle_datasets/titanic/train.csv'
test_file_path = '~/Data/kaggle_datasets/titanic/test.csv'


def remove_columns(data, excluded_cols):
    cols = set(data.columns)
    valid_cols = cols - set(excluded_cols)
    if excluded_cols:
        print("Excluded columns: ", cols.intersection(excluded_cols))
    return data[valid_cols]


def remove_strings_from_cols(data):
    num_cols = []
    strings_cols = []
    for col, dtype in data.dtypes.to_dict().items():
        if dtype.name == 'object':
            strings_cols.append(col)
        else:
            num_cols.append(col)
    if num_cols:
        print("Rejected strings columns: ", strings_cols)
        return data[num_cols]
    else:
        print("No strings columns found in the data")
        return data


def compute_simple_stats(data, name='data', include_strings=False, add_quantile=False, excluded_cols=None):
    first_msg = f"*** Stats for {name} ***"
    print("*" * len(first_msg))
    print(f"{first_msg}")
    print("*" * len(first_msg))
    if excluded_cols:
        data = remove_columns(data, excluded_cols)
    if not include_strings:
        data = remove_strings_from_cols(data)
    stats = {
        'mean': data.mean(),
        'median': data.median(),
        'std': data.std(),
        'max': data.max(),
        'min': data.min()
    }
    print()
    for s_name, s_values in stats.items():
        print(f"*** {s_name} ***")
        print(s_values, end="\n\n")
    if add_quantile:
        quantiles = [0.1, 0.3, 0.5, 0.75, 0.9]
        for q in quantiles:
            print(f"Quantile: {q}")
            print(data.quantile(q), end="\n\n")


def main():
    # Load data
    print("Loading data")
    train = pd.read_csv(train_file_path)
    test = pd.read_csv(test_file_path)

    # --------------------
    # Compute simple stats
    # --------------------
    # Mean
    compute_simple_stats(train, 'train', excluded_cols=['PassengerId'])
    print()
    compute_simple_stats(test, 'test', excluded_cols=['PassengerId'])


if __name__ == '__main__':
    main()
