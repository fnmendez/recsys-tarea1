import pandas as pd
import numpy as np
import pyreclab
import matplotlib.pyplot as plt
import scipy.sparse as sparse

# import implicit
# import scipy.sparse as sparse

views = {} # user : numer_of_interactions

fo = open("files/training.csv", "r")
fo.readline()
for line in fo.readlines():
    user, image, time = line.rstrip().split(",")
    if user in views:
        views[user] += 1
    else:
        views[user] = 1
fo.close()

user_interaction = {} # number_of_interactions : [user1, user2, ... ]

for user in views:
    if views[user] in user_interaction:
        user_interaction[views[user]].append(user)
    else:
        user_interaction[views[user]] = [user]

# get top 5
top_five = [] # user1, user2, ...
counter = 0
for key, value in sorted(views.items(), key=lambda kv: kv[1], reverse=True):
    top_five.append(key)
    counter += 1
    if counter > 4: break

# lets graph!
graph_data = [] # (number_of_interactions, number_of_users, percentage)
for k in user_interaction:
    tops_counter = 0
    total_amount_users = len(user_interaction[k])
    for user in user_interaction[k]:
        if user in top_five:
            tops_counter += 1
    percentage = 100 * float(tops_counter) / float(total_amount_users)
    # print(tops_counter, total_amount_users, user_interaction[k], top_five)
    graph_data.append((k, total_amount_users, percentage))
graph_data = sorted(graph_data)


print(graph_data)
plt.bar([i[0] for i in graph_data],[j[1] for j in graph_data])
plt.show()
