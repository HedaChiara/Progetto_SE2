import streamlit as st
import polars as pl
import json
import nltk
# nltk.download('punkt_tab')

# preparazione dei dati
@st.cache_data
def get_book_dict():
    # ho un dizionario "titolo, autore" : "descrizione"
    with open ("sf_books2.json", "r") as f:
        data = json.load(f)
    return data
data = get_book_dict()

@st.cache_data
def get_tokens(data):  
    # stoplist dell'inglese
    with open("stoplist.en.txt", "r") as f:
        stoplist = []
        for line in f:
            stoplist.append(line.strip())

    # tokenizzazione e pulizia
    for book in data.keys():
        # tokenizzazione
        data[book] = nltk.word_tokenize(data[book], language="english")
        # tolgo la punteggiatura
        data[book] = [word.lower() for word in data[book] if word.isalpha()]
        # tolgo le stop word
        data[book] = [word for word in data[book] if word not in stoplist]
        # tolgo le parole che iniziano con un carattere unicode del tipo \u1234
        data[book] = [word if not word.startswith("\\u") else word[5:] for word in data[book]]
        # tolgo le parole che iniziano con ISBN o https
        data[book] = [word for word in data[book] if not word.startswith(("ISBN", "https"))]
    return data
data = get_tokens(data)

# file di testo con le descrizioni di tutti i libri
testo = []
for descr in data.values():
    for parola in descr:
        if len(parola)>=3:
            testo.append(parola)
testo_str = " ".join(testo)
with open("descriptions.txt", "w", encoding="utf-8") as f:
    f.write(testo_str)

# stemming delle descrizioni
def stem(book_dict):
    stemmer = nltk.PorterStemmer()
    for book in book_dict.keys():
        stemmed_words = []
        for word in book_dict[book]:
            stemmed_words.append(stemmer.stem(word))
        book_dict[book] = stemmed_words
    return book_dict
stemmed = stem(data)
# salvo queste descrizioni in un file .json
with open("stemmed_descr.json", "w") as f:
    json.dump(stemmed, f)
