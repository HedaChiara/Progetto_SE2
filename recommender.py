import nltk.stem.porter
import streamlit as st
import polars as pl
import json
import nltk
import matplotlib.pyplot as plt
# nltk.download('punkt_tab')
import gensim


# preparazione dei dati
@st.cache_data
def get_data():
    # ho un dizionario "titolo" : [dizionari libri con quel titolo]
    with open ("sf_books2.json", "r") as f:
        data = json.load(f)
    # trasformo in dizionario ("titolo", "autore") : "descrizione"
    descr_dict = {}
    for k in data.keys():
        titolo_chiave = k.split(", ")
        titolo = titolo_chiave[0]
        autore = titolo_chiave[1]
        descr_dict[(titolo, autore)] = data[k]
    return descr_dict

data = get_data()
# print(data[("1984", "George Orwell")])

@st.cache_data
def get_tokens(data):  
    # stoplist dell'inglese
    with open("stoplist.en.txt", "r") as f:
        stoplist = []
        for line in f:
            stoplist.append(line.strip())

    # tokenizzazione e un po' di pulizia
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
        # stemming
        stemmer = nltk.PorterStemmer()
        data[book] = [stemmer.stem(word) for word in data[book]]
    return data

data = get_tokens(data)


#### RECOMMENDER SYSTEM
# Modello con doc2vec
# fonti:
# https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.Doc2Vec
# https://stackoverflow.com/questions/42781292/doc2vec-get-most-similar-documents
# preparo i documenti da dare in input al modello (vuole dei TaggedDocument)
docs = []
for book in data.keys():
    docs.append(gensim.models.doc2vec.TaggedDocument(words=data[book], tags=[book]))
# modello
model = gensim.models.doc2vec.Doc2Vec(docs)
# vettore del libro 1984
orw1984 = model.infer_vector(data[("1984", "George Orwell")])
# stampo i 10 libri più simili a 2984
print(model.docvecs.most_similar(positive=[orw1984], topn=10))

