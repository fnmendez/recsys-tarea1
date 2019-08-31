import pandas as pd
import numpy as np
import pyreclab
import matplotlib.pyplot as plt
import scipy.sparse as sparse

# import implicit
# import scipy.sparse as sparse

df_train = pd.read_csv('files/training.csv',
                        sep="\t")
print(df_train.head())

photos_per_user = {} # {}
