import pandas as pd
import numpy as np
import pyreclab
import matplotlib.pyplot as plt
import scipy.sparse as sparse

# import implicit
# import scipy.sparse as sparse

df_train = pd.read_csv('files/training.csv',
                        sep=",",
                        )

print(df_train.head())
print(df_train.columns)

photos_by_user = df_train.groupby(['user']).count()[['image_id']]
# se le deberia cambiar el nombre a la columna
print(photos_by_user)
print(photos_by_user.columns)


#print(photos_by_user)
