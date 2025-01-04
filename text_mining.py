import streamlit as st
import polars as pl
import json
import nltk
import wordcloud
import matplotlib.pyplot as plt
# nltk.download('punkt_tab')
# import gensim

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
        data[book] = nltk.word_tokenize(data[book], language="english")
        # tolgo la punteggiatura
        data[book] = [word.lower() for word in data[book] if word.isalpha()]
        # tolgo le stop word
        data[book] = [word for word in data[book] if word not in stoplist]
        # tolgo le parole che iniziano con un carattere unicode del tipo \u1234
        data[book] = [word if not word.startswith("\\u") else word[5:] for word in data[book]]
        # tolgo le parole che iniziano con ISBN
        #data[book] = [word if not word.startswith("ISBN") else word[5:] for word in data[book]]
    # togliere parole che iniziano con https
    
    # a volte dopo certe parole c'è \u*numero*... a volte anche prima... <- sono simboli di punteggiatura in unicode:
    # quando sono attaccati ad una parola all'inizio o alla fine, mantiene la parola e toglie il simbolo
    # invece se è nel mezzo tra due parole, toglie entrambe (es: again Grand in ("Bold", "Mike Shepherd"))
    return data

data = get_tokens(data)
print(data[("1984", "George Orwell")])
print(data[("Bold", "Mike Shepherd")])

# file di testo con le descrizioni di tutti i libri
testo = []
for descr in data.values():
    for parola in descr:
        if len(parola)>=3:
            testo.append(parola)
testo_str = " ".join(testo)
with open("descriptions.txt", "w", encoding="utf-8") as f:
    f.write(testo_str)







