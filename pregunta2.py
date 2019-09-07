import implicit
import pandas as pd
import numpy as np
import matplotlib as plt
import scipy.sparse as sparse

import metrics

metrics = metrics.Metrics()

TRAIN_FILE = 'data/new_training_set.csv'
TEST_FILE = 'data/new_testing_set.csv'

def evaluate_model(model, n):
  mean_map = 0.
  mean_ndcg = 0.
  for u in range(len(user_items)): # para cada user_id
    rec = [t[0] for t in model.recommend(user_ids[u], user_item_matrix, n)]
    rel_vector = [np.isin(user_items_test[user_ids_inv[u]], rec, assume_unique=True).astype(int)]
    mean_map += metrics.mean_average_precision(rel_vector)
    mean_ndcg += metrics.ndcg_at_k(rel_vector, n)

  mean_map /= len(user_items_test)
  mean_ndcg /= len(user_items_test)

  return mean_map, mean_ndcg

def show_recommendations(model, user, n):
  recommendations = [t[0] for t in model.recommend(user, user_item_matrix, n)]
  return recommendations

def show_similar_item(model, item, n=10):
  sim_items = [t[0] for t in model.similar_items(item, n)]
  return sim_items


df_train = pd.read_csv(TRAIN_FILE, names=['userid', 'itemid', 'timestamp'])
df_test = pd.read_csv(TEST_FILE, names=['userid', 'itemid', 'timestamp'])

user_items_test = {} # {userid: [imageid1, imageid2, ... ]}

for row in df_test.itertuples():
    if row[1] not in user_items_test:
        user_items_test[row[1]] = []
    user_items_test[row[1]].append(row[2])

# PROCESAMIENTO DE LOS DATOS A FORMATO SPARSE
user_items = {} # {userid: [imageid1, imageid2, ... ]}
itemset = set() # {imageid1, imageid2, imageid3, ... }

for row in df_train.itertuples():
    if row[1] not in user_items:
        user_items[row[1]] = []
    user_items[row[1]].append(row[2])
    itemset.add(row[2])

itemset = np.sort(list(itemset)) # todos los items ordenados en un set
userset = np.sort(list(user_items.keys())) # todos los users ordenados en un set

sparse_matrix = np.zeros((len(user_items), len(itemset))) # matriz de nxm llena de 0s
user_ids = {key: i for i, key in enumerate(userset)} # user_id: numero_file_en_la_matriz
user_ids_inv = {i: key for i, key in enumerate(userset)} # numero_file_en_la_matriz: user_id:

items_ids = {key: i for i, key in enumerate(itemset)} # item_id: numero_columna_en_la_matriz
items_ids_inv = {i: key for i, key in enumerate(itemset)} # numero_columna_en_la_matriz: item_id

for i in range(len(user_items)):
    sparse_matrix[i] = np.isin(itemset, user_items[user_ids_inv[i]], assume_unique=True).astype(int)

matrix = sparse.csr_matrix(sparse_matrix.T)
user_item_matrix = matrix.T.tocsr()
# FIN PROCESAMIENTO DE LOS DATOS A FORMATO SPARSE

# ALS
model_als = implicit.als.AlternatingLeastSquares(
                            factors=100,
                            regularization=0.01,
                            iterations=15,
                            use_gpu=False) # ALS with default values
model_als.fit(matrix)

show_recommendations(model_als, user=71, n=10)
maprec, ndcg = evaluate_model(model_als, n=10)
print('map: {}\nndcg: {}'.format(maprec, ndcg))
