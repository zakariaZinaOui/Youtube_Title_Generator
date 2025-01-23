import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import pickle

def load_and_preprocess_data():
    # Charger les données
    df = pd.read_csv('USvideos.csv')
    titles = df['title'].astype(str).values
    
    # Tokenisation
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(titles)
    total_words = len(tokenizer.word_index) + 1
    
    # Création des séquences d'entrée-sortie
    input_sequences = []
    for title in titles:
        token_list = tokenizer.texts_to_sequences([title])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)
    
    # Padding des séquences
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
    
    # Création des données X et y
    X = input_sequences[:, :-1]
    y = input_sequences[:, -1]
    
    return X, y, tokenizer, total_words, max_sequence_len

def create_model(total_words, max_sequence_len):
    model = Sequential([
        Embedding(total_words, 100, input_length=max_sequence_len-1),
        LSTM(150),
        Dense(total_words, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', 
                 optimizer='adam', 
                 metrics=['accuracy'])
    return model

def train_and_save_model():
    print("Chargement et prétraitement des données...")
    X, y, tokenizer, total_words, max_sequence_len = load_and_preprocess_data()
    
    print("Création du modèle...")
    model = create_model(total_words, max_sequence_len)
    
    print("Entraînement du modèle...")
    model.fit(X, y, epochs=20, batch_size=128, verbose=1)
    
    print("Sauvegarde du modèle et du tokenizer...")
    model.save('youtube_title_model.h5')
    with open('tokenizer.pkl', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("Terminé !")

if __name__ == "__main__":
    train_and_save_model()
