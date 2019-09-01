import pandas as pd
import numpy as np
import pyreclab
import matplotlib.pyplot as plt
import scipy.sparse as sparse

# import implicit
# import scipy.sparse as sparse

df_train = pd.read_csv('files/training.csv')

# usuarios y cantidad de imagenes que vieron
photos_by_user = df_train.groupby(['user']).count()[['image_id']].reset_index()

# ordenar y ver los 5 que vieron los mas grandes
top_five = photos_by_user.sort_values(by=['image_id'], ascending=False).iloc[:5]
print(top_five)



# cantidad de usuarios y cantidad de interacciones
p = photos_by_user.groupby(['image_id']).count()[['user']].reset_index()
p.columns = ['times_rated', 'amount_users']
print(p.head())





# imagen y la cantidad de usuarios que la vieron
users_by_photo = df_train.groupby(['image_id']).count()[['user']].reset_index()

# ordenar y ver las 5 imagenes mas vistas
image_top_five = users_by_photo.sort_values(by=['user'], ascending=False).iloc[:5]


print(image_top_five.head())
