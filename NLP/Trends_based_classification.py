from keras import initializers
import tensorflow as tf
from files_reader import *
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.utils import to_categorical
import tensorflow as tf
import pickle
from time import ctime
from lemmatizer_and_stemmer import LemmatizerAndStemmer


#Get the data
tweets_and_trends = []
tweets = []
trends = []

tweets_and_trends += (FilesReader.read_file(new_US_file))
tweets_and_trends += (FilesReader.read_file(new_UK_file))
tweets_and_trends += (FilesReader.read_file(new_AUS_file))
tweets_and_trends += (FilesReader.read_file(new_CAN_file))
tweets_and_trends += (FilesReader.read_file(new_IR_file))

random.shuffle(tweets_and_trends)

tweets, trends = FilesReader.split_tweets_and_trends(tweets_and_trends)

for i, tweet in enumerate(tweets):
    processed_tweet = LemmatizerAndStemmer.stem_and_lemmatize_tweet(tweet)
    tweets[i] = processed_tweet

tweets_tokenizer = Tokenizer(oov_token="<OOV>")
tweets_tokenizer.fit_on_texts(tweets)
tweets_word_index = tweets_tokenizer.word_index
tweets_index_word = tweets_tokenizer.index_word

#Create the padded sequences
sequence_length = 15

tweets_sequences = tweets_tokenizer.texts_to_sequences(tweets)
tweets_sequences_padded = pad_sequences(tweets_sequences, padding="post", maxlen=sequence_length)


#Map the trends to numbers
trends_map = {}

counter = 0

for trend in trends:
    if not (trend in trends_map):
        trends_map[trend] = counter
        counter += 1

no_of_trends = len(trends_map)
inv_trends_map = {v: k for k, v in trends_map.items()}


#Create the trends sequences
trends_sequences = [trends_map[trend] for trend in trends]


#Encode the trends
encoded_trends = to_categorical(trends_sequences)


#Prepare the pre-trained embeddings
from Embeddings.embeddings_matrix import get_embeddings_matrix

embeddings_index_path = "./NLP/Embeddings/embeddings_index_object.pkl"
embeddings_matrix, hits, misses = get_embeddings_matrix(tweets_word_index, embeddings_index_path)


#Split the data
training_split = 0.8
training_tweets_count = int(0.8 * len(tweets_sequences_padded))

train_data = tweets_sequences_padded[0:training_tweets_count]
train_labels = encoded_trends[0:training_tweets_count]
test_data = tweets_sequences_padded[training_tweets_count:]
test_labels = encoded_trends[training_tweets_count:]


#Build the model

#hyperparameters
embedding_dimensions = 300
lstm_units = 144
dropout_value = 0.1
conv_filters = 224
conv_kernel_size = 2

no_of_tweets_words = len(tweets_word_index) + 1

trends_classifier = tf.keras.Sequential([
    tf.keras.layers.Embedding(
        no_of_tweets_words,
        embedding_dimensions,
        input_length=sequence_length,
        embeddings_initializer=initializers.Constant(embeddings_matrix),
        trainable=True
    ),
    tf.keras.layers.Conv1D(conv_filters, conv_kernel_size, activation='relu'),
    tf.keras.layers.AveragePooling1D(),
    tf.keras.layers.Dropout(dropout_value),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units, activation='tanh')),
    tf.keras.layers.Dropout(dropout_value),
    tf.keras.layers.Dense(no_of_trends, activation='softmax')
])

trends_classifier.compile(
    loss="categorical_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)


#Train the model
epochs = 4
history = trends_classifier.fit(train_data, train_labels, epochs=epochs, validation_data=(test_data, test_labels))


#Save the model
trends_classifier.save("./NLP/trends_classifier/trends_classifier_model.h5")
with open('./NLP/trends_classifier/inv_trends_map.pkl', 'wb') as output:
    pickle.dump(inv_trends_map, output)
with open('./NLP/trends_classifier/tweet_tokenizer.pkl', 'wb') as output:
    pickle.dump(tweets_tokenizer, output)

with open('./NLP/model_report.txt', 'a') as output:
    output.write(f"{ctime()}: {history.history['val_accuracy']}, trained on {len(tweets)} tweets, {no_of_trends} trends\n")

