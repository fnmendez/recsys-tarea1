import implicit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sparse
import time

import metrics

metrics = metrics.Metrics()

TRAIN_FILE = 'data/new_training_set.csv'
TEST_FILE = 'data/new_testing_set.csv'

def evaluate_model(model, n):
  mean_map = 0.
  mean_ndcg = 0.
  for u in range(len(user_items)): # para cada user_id en el training
    rec = [t[0] for t in model.recommend(u, user_item_matrix, n)]
    user_item_test_list = [items_ids[i] for i in user_items_test[user_ids_inv[u]]] # lista con las peliculas que vio en el test
    rel_vector = [np.isin(user_item_test_list, rec, assume_unique=True).astype(int)]
    mean_map += metrics.mean_average_precision(rel_vector)
    mean_ndcg += metrics.ndcg_at_k(rel_vector, n)

  mean_map /= len(user_items_test)
  mean_ndcg /= len(user_items_test)

  return mean_map, mean_ndcg

def show_recommendations(model, user, n):
  recommendations = [items_ids_inv[t[0]] for t in model.recommend(user, user_item_matrix, n)]
  return recommendations

def show_similar_item(model, item, n=10):
  sim_items = [t[0] for t in model.similar_items(item, n)]
  return sim_items


df_train = pd.read_csv(TRAIN_FILE, names=['userid', 'itemid', 'timestamp'])
df_test = pd.read_csv(TEST_FILE, names=['userid', 'itemid', 'timestamp'])

# TEST USER ITEM
user_items_test = {} # {userid: [imageid1, imageid2, ... ]}
for row in df_test.itertuples():
    if row[1] not in user_items_test:
        user_items_test[row[1]] = []
    user_items_test[row[1]].append(row[2])

# PROCESAMIENTO DE LOS DATOS A FORMATO SPARSE
user_items = {} # TRAIN - {userid: [imageid1, imageid2, ... ]}
itemset = set() # {imageid1, imageid2, imageid3, ... }

for row in df_train.itertuples():
    if row[1] not in user_items:
        user_items[row[1]] = []
    user_items[row[1]].append(row[2])
    itemset.add(row[2])

for row in df_test.itertuples():
    itemset.add(row[2])



itemset = np.sort(list(itemset)) # todos los items ordenados en un set
userset = np.sort(list(user_items.keys())) # todos los users ordenados en un set

user_ids = {key: i for i, key in enumerate(userset)} # user_id: numero_file_en_la_matriz
user_ids_inv = {i: key for i, key in enumerate(userset)} # numero_file_en_la_matriz: user_id:

items_ids = {key: i for i, key in enumerate(itemset)} # item_id: numero_columna_en_la_matriz
items_ids_inv = {i: key for i, key in enumerate(itemset)} # numero_columna_en_la_matriz: item_id

sparse_matrix = np.zeros((len(user_items), len(itemset))) # matriz de nxm llena de 0s

for i in range(len(user_items)):
    sparse_matrix[i] = np.isin(itemset, user_items[user_ids_inv[i]], assume_unique=True).astype(int)

matrix = sparse.csr_matrix(sparse_matrix.T)
user_item_matrix = matrix.T.tocsr()
# FIN PROCESAMIENTO DE LOS DATOS A FORMATO SPARSE

# ALS

# tiempos e hiperparametros
test_factors = [50, 100, 200, 500, 1000]
test_iterations = [15, 20, 60, 140, 200]
test_regulazation = [0.01, 0.1, 0.15, 0.2, 0.5]

test_lr = [0.001, 0.01, 0.02, 0.05]

def graph_als_test_factors():
    maprec_results = []
    ndcg_results = []
    for f in test_factors:
        my_time = time.time()
        # iterations default number is 15
        model_als = implicit.als.AlternatingLeastSquares(factors=f)
        model_als.fit(matrix)
        maprec, ndcg = evaluate_model(model_als, n=10)
        maprec_results.append(maprec)
        ndcg_results.append(ndcg)
        recommendations = show_recommendations(model_als, 0, 5)
        print("recomendaciones als factor: ", f, recommendations)
        my_time = time.time() - my_time
        print("timepo de entrenamiento als facotr: ",f, my_time)

    print("maprec: ", maprec_results)
    print("ndcg: ", ndcg_results)

    plt.plot(test_factors, maprec_results, 'r-')
    plt.xlabel('factor latente', fontsize=15)
    plt.ylabel('map@10', fontsize=15)
    plt.show()

    plt.plot(test_factors, ndcg_results, 'b-')
    plt.xlabel('factor latente', fontsize=15)
    plt.ylabel('nDCG@10', fontsize=15)
    plt.show()

def graph_als_test_iterations():
    maprec_results = []
    ndcg_results = []
    for i in test_iterations:
        # iterations default number is 15
        my_time = time.time()
        model_als = implicit.als.AlternatingLeastSquares(iterations=i)
        model_als.fit(matrix)
        maprec, ndcg = evaluate_model(model_als, n=10)
        maprec_results.append(maprec)
        ndcg_results.append(ndcg)
        recommendations = show_recommendations(model_als, 0, 5)
        print("recomendaciones: ", i,":", recommendations)
        my_time = time.time() - my_time
        print("timepo: ",i,":", my_time)

    print(maprec_results)
    print(ndcg_results)

    plt.plot(test_iterations, maprec_results, 'r-')
    plt.xlabel('numero de iteraciones', fontsize=15)
    plt.ylabel('map@10', fontsize=15)
    plt.show()

    plt.plot(test_iterations, ndcg_results, 'b-')
    plt.xlabel('numero de iteraciones', fontsize=15)
    plt.ylabel('nDCG@10', fontsize=15)
    plt.show()

def graph_als_test_regulazation():
    maprec_results = []
    ndcg_results = []
    for r in test_regulazation:
        # iterations default number is 15
        my_time = time.time()
        model_als = implicit.als.AlternatingLeastSquares(regularization=r)
        model_als.fit(matrix)
        maprec, ndcg = evaluate_model(model_als, n=10)
        maprec_results.append(maprec)
        ndcg_results.append(ndcg)
        recommendations = show_recommendations(model_als, 0, 5)
        print("recomendaciones: ", r,":", recommendations)
        my_time = time.time() - my_time
        print("timepo: ",r,":", my_time)

    print(maprec_results)
    print(ndcg_results)

    plt.plot(test_regulazation, maprec_results, 'r-')
    plt.xlabel('regularization', fontsize=15)
    plt.ylabel('map@10', fontsize=15)
    plt.show()

    plt.plot(test_regulazation, ndcg_results, 'b-')
    plt.xlabel('regularization', fontsize=15)
    plt.ylabel('nDCG@10', fontsize=15)
    plt.show()

# BPR

def graph_bpr_test_factors():
    maprec_results = []
    ndcg_results = []
    for f in test_factors:
        my_time = time.time()
        model_bpr = implicit.bpr.BayesianPersonalizedRanking(factors=f)
        model_bpr.fit(matrix)
        maprec, ndcg = evaluate_model(model_bpr, n=10)
        maprec_results.append(maprec)
        ndcg_results.append(ndcg)
        recommendations = show_recommendations(model_bpr, 0, 5)
        print("recomendaciones: ", f,":", recommendations)
        my_time = time.time() - my_time
        print("timepo: ",f,":", my_time)

    plt.plot(test_factors, maprec_results, 'r-')
    plt.xlabel('factor latente', fontsize=15)
    plt.ylabel('map@10', fontsize=15)
    plt.show()

    plt.plot(test_factors, ndcg_results, 'b-')
    plt.xlabel('factor latente', fontsize=15)
    plt.ylabel('nDCG@10', fontsize=15)
    plt.show()

def graph_bpr_test_iterations():
    maprec_results = []
    ndcg_results = []
    for i in test_iterations:
        my_time = time.time()
        model_bpr = implicit.bpr.BayesianPersonalizedRanking(iterations=i)
        model_bpr.fit(matrix)
        maprec, ndcg = evaluate_model(model_bpr, n=10)
        maprec_results.append(maprec)
        ndcg_results.append(ndcg)
        recommendations = show_recommendations(model_bpr, 0, 5)
        print("recomendaciones: ", i,":", recommendations)
        my_time = time.time() - my_time
        print("timepo: ",i,":", my_time)

    plt.plot(test_iterations, maprec_results, 'r-')
    plt.xlabel('iteraciones', fontsize=15)
    plt.ylabel('map@10', fontsize=15)
    plt.show()

    plt.plot(test_iterations, ndcg_results, 'b-')
    plt.xlabel('iteraciones', fontsize=15)
    plt.ylabel('nDCG@10', fontsize=15)
    plt.show()

def graph_bpr_test_regulazation():
    maprec_results = []
    ndcg_results = []
    for r in test_regulazation:
        my_time = time.time()
        model_bpr = implicit.bpr.BayesianPersonalizedRanking(regularization=r)
        model_bpr.fit(matrix)
        model_bpr.fit(matrix)
        maprec, ndcg = evaluate_model(model_bpr, n=10)
        maprec_results.append(maprec)
        ndcg_results.append(ndcg)
        recommendations = show_recommendations(model_bpr, 0, 5)
        print("recomendaciones: ", r,":", recommendations)
        my_time = time.time() - my_time
        print("tiempo: ",r,":", my_time)

    plt.plot(test_regulazation, maprec_results, 'b-')
    plt.xlabel('regularization', fontsize=15)
    plt.ylabel('map@10', fontsize=15)
    plt.show()

    plt.plot(test_regulazation, ndcg_results, 'b-')
    plt.xlabel('regularization', fontsize=15)
    plt.ylabel('nDCG@10', fontsize=15)
    plt.show()

def graph_bpr_test_lr():
    maprec_results = []
    ndcg_results = []
    for l in test_lr:
        my_time = time.time()

        model_bpr = implicit.bpr.BayesianPersonalizedRanking(learning_rate=l)

        model_bpr.fit(matrix)
        maprec, ndcg = evaluate_model(model_bpr, n=10)
        maprec_results.append(maprec)
        ndcg_results.append(ndcg)
        recommendations = show_recommendations(model_bpr, 0, 5)
        print("recomendaciones: ", l,":", recommendations)
        my_time = time.time() - my_time
        print("tiempo: ",l,":", my_time)

    plt.plot(test_lr, maprec_results, 'r-')
    plt.xlabel('learning rate', fontsize=15)
    plt.ylabel('map@10', fontsize=15)
    plt.show()

    plt.plot(test_lr, ndcg_results, 'b-')
    plt.xlabel('learning rate', fontsize=15)
    plt.ylabel('nDCG@10', fontsize=15)
    plt.show()

def compare_best_models():
    model_als = implicit.als.AlternatingLeastSquares(
                            factors=50,
                            iterations = 140,
                            regularization=0.15)

    model_als.fit(matrix)
    maprec, ndcg = evaluate_model(model_als, n=10)
    print("A",maprec, ndcg)

    model_bpr = implicit.bpr.BayesianPersonalizedRanking(
                            factors=150,
                            iterations = 15,
                            regularization=0.15,
                            learning_rate=0.01)
    model_bpr.fit(matrix)
    maprec, ndcg = evaluate_model(model_bpr, n=10)
    print("B",maprec, ndcg)

def write_recommendations_best_model():
    model_bpr = implicit.bpr.BayesianPersonalizedRanking(
                            factors=150,
                            iterations = 15,
                            regularization=0.5,
                            learning_rate=0.01)
    model_bpr.fit(matrix)

    fo = open("files/test.csv", "r")
    fw = open("results.json", "w+")
    fw.write("{\n")
    fo.readline()
    for u in fo.readlines():
        u = int(u.strip())
        nu = user_ids[u]
        recommendations = show_recommendations(model=model_bpr, user=nu, n=10)
        fw.write('"'+str(u)+'"'+": ")
        fw.write(str(recommendations) + "," + "\n")

    fw.write("}\n")
    fw.close()
    fo.close()

write_recommendations_best_model()

"""
graph_als_test_iterations()
graph_als_test_regulazation()
graph_bpr_test_factors()
graph_bpr_test_iterations()
graph_bpr_test_regulazation()
graph_bpr_test_lr()
"""
