import json
import pandas as pd
from ast import literal_eval
from sklearn.decomposition import PCA

EMBEDDINGS_FILE = 'files/image_embeddings.json'

# with open(EMBEDDINGS_FILE) as json_data:
#     raw_data = json.load(json_data)
#
# _X = pd.DataFrame.from_dict(raw_data, orient='index')
#
# indexes = list(map(lambda x: int(x), list(_X.index)))
# embeddings = list(map(lambda x: literal_eval(x[0]), list(_X.values)))
#
# tuples = list(zip(indexes, embeddings))
# df = pd.DataFrame(tuples, columns=['id', 'embedding'])
# df.to_csv("./data/image_embeddings.csv")

with open(EMBEDDINGS_FILE) as infile, open('clean_embeddings.json', 'w') as outfile:
    data = infile.read()
    data = data.replace('"', "")
    outfile.write(data)
