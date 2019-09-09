import pandas as pd
from sklearn.decomposition import PCA

EMBEDDINGS_FILE = 'files/image_embeddings.json'

with open(EMBEDDINGS_FILE) as json_data:
    _X = pd.read_json(json_data)

pca = PCA(n_components=3)
pca.fit(_X)
