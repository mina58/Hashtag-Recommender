import numpy as np
import pickle

glove_path = './glove.840B.300d/glove.840B.300d.txt'

embeddings_index = {}
with open(glove_path, encoding='utf-8') as f:
    for line in f:
        word, coefs = line.split(maxsplit=1)
        coefs = np.fromstring(coefs, "f", sep=" ")
        embeddings_index[word] = coefs

print("Found %s word vectors." % len(embeddings_index))

with open('./embeddings_index_object.pkl', 'wb') as output:
    pickle.dump(embeddings_index, output)