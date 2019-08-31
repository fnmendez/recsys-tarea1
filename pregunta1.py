import pandas as pd
import numpy as np
import pyreclab
import matplotlib.pyplot as plt
import scipy.sparse as sparse

# import implicit
# import scipy.sparse as sparse

df_train = pd.read_csv('files/training.csv',
                        sep="\t",
                        header=0,
                        )
print(df_train.head())


#df.groupby(['userid']).count()
