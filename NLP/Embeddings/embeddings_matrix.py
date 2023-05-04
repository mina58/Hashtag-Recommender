import pickle
import numpy as np

def get_embeddings_matrix(tweets_word_index, embeddings_index_path):
    num_tokens = len(tweets_word_index) + 1
    embedding_dim = 300
    hits = 0
    misses = 0

    embedding_matrix = np.zeros((num_tokens, embedding_dim))
    with open(embeddings_index_path, 'rb') as embeddings_file:
        embeddings_index = pickle.load(embeddings_file)
        for word, i in tweets_word_index.items():
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                # Words not found in embedding index will be all-zeros.
                # This includes the representation for "padding" and "OOV"
                if embedding_vector.shape == (300,):
                    embedding_matrix[i] = embedding_vector
                hits += 1
            else:
                misses += 1

    return embedding_matrix, hits, misses