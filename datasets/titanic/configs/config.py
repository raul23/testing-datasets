# ---------------
# General options
# ---------------
quiet = False
verbose = True

# --------------
# Data filepaths
# --------------
data_filepath = None
train_filepath = '~/Data/kaggle_datasets/titanic/train.csv'
valid_filepath = None
test_filepath = '~/Data/kaggle_datasets/titanic/test.csv'
y_target = 'Survived'

# -------------
# Compute stats
# -------------
data_stats= True,
train_stats= True,
valid_stats= True,
test_stats= True,
excluded_cols= ['PassengerId']

# ------------------
# HEAD: first N rows
# ------------------
data_head = 5
train_head = 5
valid_head = 5
test_head = 5

# ------------------------------
# Count number of missing values
# ------------------------------
data_isnull = True
train_isnull = True
valid_isnull = True
test_isnull = True

# ----------------
# Tree-based model
# ----------------
trees_models = {
    'model_name': 'RandomForestClassifier',
    'model_params': {
        'n_estimators': 100,
        'max_depth': 5,
        'random_state': 1
    },
    'features': ["Pclass", "Sex", "SibSp", "Parch"]
}
