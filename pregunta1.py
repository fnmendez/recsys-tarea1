import pandas as pd
import numpy as np
import pyreclab
import matplotlib.pyplot as plt
import scipy.sparse as sparse
import math

# import implicit
# import scipy.sparse as sparse

views = {} # user : numer_of_interactions
image_views = {} # image: number_of_interactions

fo = open("files/training.csv", "r")
fo.readline()
for line in fo.readlines():
    user, image, time = line.rstrip().split(",")
    if user in views:
        views[user] += 1
    else:
        views[user] = 1

    if image in image_views:
        image_views[image] +=1
    else:
        image_views[image] = 1
fo.close()

user_interaction = {} # number_of_interactions : amount_of_users
for user in views:
    if views[user] in user_interaction:
        user_interaction[views[user]] += 1
    else:
        user_interaction[views[user]] = 1

image_interaction = {} # number_of_interactions : amount_of_images
for image in image_views:
    if image_views[image] in image_interaction:
        image_interaction[image_views[image]] += 1
    else:
        image_interaction[image_views[image]] = 1

# get top
top_five_users = [] # user1, user2, ...
counter = 0
for key, value in sorted(views.items(), key=lambda kv: kv[1], reverse=True):
    top_five_users.append(key)
    counter += 1
    if counter > 4: break

top_five_image = [] # user1, user2, ...
counter = 0
for key, value in sorted(image_views.items(), key=lambda kv: kv[1], reverse=True):
    top_five_image.append(key)
    counter += 1
    if counter > 4: break
# finish get top 5


# stats
total_number_of_interactions = sum(views[u] for u in views)
number_of_different_users = len(views)
number_of_different_images = len(image_views)
mean_image_per_user = sum(views[u] for u in views) / number_of_different_users
de_image_per_user = math.sqrt((sum((views[u] - mean_image_per_user)**2 for u in views))/number_of_different_users)
mean_user_per_image = sum(image_views[i] for i in image_views) / number_of_different_images
de_user_per_image = math.sqrt((sum((image_views[i] - mean_user_per_image)**2 for i in image_views))/number_of_different_images)
density = total_number_of_interactions / (number_of_different_users * number_of_different_images)
sparsity = 1 - density

print("stats:")
print("number of users:", number_of_different_users)
print("number of images:", number_of_different_images)
print("mean_image_per_user:", mean_image_per_user)
print("de_image_per_user:", de_image_per_user)
print("mean_user_per_image:", mean_user_per_image)
print("de_user_per_image:", de_user_per_image)
print("density:", density)
print("sparsity:", sparsity)
# finish stats


# lets graph!
user_graph_data = [] # (number_of_interactions, number_of_users rango de 3)
for k in user_interaction:
    user_graph_data.append((k, user_interaction[k]))
user_graph_data = sorted(user_graph_data)

image_graph_data = []
for k in image_interaction:
    image_graph_data.append((k, image_interaction[k]))
image_graph_data = sorted(image_graph_data)

# aca agrupamos la info para que no sea tan grande
new_graph_data = [] # ('0-3', 74), ('4-7', 95)
x_name = ''
count = 0
counter = 0
for x, y in user_graph_data:
    counter += y
    if count == 0:
        x_name = str(x) + '-'
    if count == 3:
        x_name += str(x)
        new_graph_data.append((x_name, counter))
        count = -1
        counter = 0
    count += 1

plt.bar([i[0] for i in new_graph_data], [j[1] for j in new_graph_data])
plt.xlabel('Numero de interacciones', fontsize=15)
plt.ylabel('Numero de usuarios', fontsize=15)
plt.xticks([i[0] for i in new_graph_data], [i[0] for i in new_graph_data], rotation=70)
plt.plot([i[0] for i in new_graph_data], [j[1] for j in new_graph_data], 'r-')
plt.show()

# simple graph
plt.bar([i[0] for i in user_graph_data], [j[1] for j in user_graph_data])
plt.xlabel('Numero de interacciones', fontsize=15)
plt.ylabel('Numero de usuarios', fontsize=15)
plt.plot([i[0] for i in user_graph_data], [j[1] for j in user_graph_data], 'r-')
plt.show()
print("los 5 usuarios mas activos son :", top_five_users)

total_interactions = 0
interactions_made_by_top_5_users = 0
interactions_in_top_5_images = 0

for user in views:
    total_interactions += views[user]
    if user in top_five_users:
        interactions_made_by_top_5_users += views[user]
print("total_interactions: ", total_interactions)
print("made by top 5 users", interactions_made_by_top_5_users)
percent_user = 100 * interactions_made_by_top_5_users / total_interactions
print("percent made by top 5 users", percent_user)

for image in image_views:
    if image in top_five_image:
        interactions_in_top_5_images += image_views[image]
percent_imaage = 100 * interactions_in_top_5_images / total_interactions
print("percent of image", percent_imaage)

print("made by in top 5 images", interactions_in_top_5_images)


plt.xlabel('Numero de interacciones', fontsize=15)
plt.ylabel('Numero de imagenes', fontsize=15)
plt.bar([i[0] for i in image_graph_data], [j[1] for j in image_graph_data])
plt.plot([i[0] for i in image_graph_data], [j[1] for j in image_graph_data], 'r--')
plt.show()
print("los 5 imagenes mas vistas son :", top_five_image)
