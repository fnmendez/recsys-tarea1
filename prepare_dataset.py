import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train_frac = .8

df_train = pd.read_csv('files/training.csv')

df_per_user = df_train.groupby(['user']).count()[['image_id']].reset_index() # userid, count_visits
df_per_user.columns = ['user_id', 'visits']

def separate(data):
    print('Separating data...')
    users_ids = pd.unique(data['user'])
    train_set = pd.DataFrame(None, columns = ['user', 'image_id', 'timestamp'])
    test_set = pd.DataFrame(None, columns = ['user', 'image_id', 'timestamp'])

    for id in users_ids:
        visit_count = int(df_per_user[df_per_user['user_id'] == id]['visits'])
        if visit_count < 2:
            continue
        n_train = int(visit_count * train_frac)
        train_set = pd.concat([train_set, data[data['user'] == id][:n_train]])
        test_set = pd.concat([test_set, data[data['user'] == id][n_train:]])
    return train_set, test_set

train, test = separate(df_train)
train.to_csv("./data/training_set.csv")
test.to_csv("./data/testing_set.csv")
