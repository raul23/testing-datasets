quiet = False
verbose = True

data_filepath = ''
train_filepath = '~/Data/kaggle_datasets/titanic/train.csv'
valid_filepath = ''
test_filepath = '~/Data/kaggle_datasets/titanic/test.csv'

compute_stats = {
    'for_data': True,
    'for_train': True,
    'for_valid': True,
    'for_test': True,
    'excluded_cols': ['PassengerId']
}

data_head = 5
train_head = 5
valid_head = 5
test_head = 5

data_isnull = True
train_isnull = True
valid_isnull = True
test_isnull = True

trees_models = {
    'model_name': 'RandomForestClassifier',
    'model_params': {
    }
}