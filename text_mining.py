import streamlit as st
import polars as pl
import json
import nltk
# nltk.download('punkt_tab')
import gensim

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
    # togliere parole che iniziano con ISBN, https ecc...

    # a volte dopo certe parole c'è \u*numero*... a volte anche prima... <- sono simboli di punteggiatura in unicode:
    # quando sono attaccati ad una parola all'inizio o alla fine, mantiene la parola e toglie il simbolo
    # invece se è nel mezzo tra due parole, toglie entrambe (es: again Grand in ("Bold", "Mike Shepherd"))
    return data

data = get_tokens(data)
print(data[("1984", "George Orwell")])
print(data[("Bold", "Mike Shepherd")])

# quali sono le parole più frequenti in queste descrizioni? Faccio un unico testo lunghissimo e poi conto (vedi Lab1)
testo = []
for descr in data.values():
    for parola in descr:
        testo.append(parola)
# ha senso eliminare le parole troppo frequenti e quelle troppo poco frequenti?

# stemming




# provare: 
# - k-means -> vedere che raggruppamenti fa, per cosa si differenziano i gruppi e cercare di darci un senso (quanti gruppi?)
# - clustering gerarchico
# ma come faccio ad utilizzare questi metodi partendo da parole e non da variabili quantitative? Con TF-IDF immagino
# - word2vec -> trovo i libri più simili al mio libro di input in base a cosine similarity o simili
#   posso provare a fare clustering tenendo conto anche dei generi e dell'autore (se dello stesso autore, aumenta la similarità)
# - information retrieval -> trovo i libri più pertinenti ad una certa frase di input (es: libri distopici ambientati nel futuro)
#   chiedere quanti se ne vogliono visualizzare al massimo (minimo no, che magari non ce ne sono abbastanza)
#   come migliorare? Posso tenere conto del sottogenere di un libro?
#   se nella query ho "famosi", filtrare secondo numero di valutazioni, se mi dice "di nicchia" pure, ecc...
#   se mi dice "di autrici donne" bla bla bla...
#   potrei fare un po' di giudizi di rilevanza a mano per usare il mio miglioramento, ma è lunga la storia, sempre che non riesca a fare
#   un sistema di rilevazione semi-automatico della rilevanza (a partire dalle trame)
# miglioramenti:
# - migliorare le descrizioni -> potrei chiedere a chatgpt di riassumermi i libri, in questo genere di cose solitamente fa bene

# Documento i vari tentativi e scelgo il migliore (come?)



# IN VISTA DELLA TESI
# dai un occhio a https://www.goodreads.com/api, https://openlibrary.org/developers, https://www.gutenberg.org/ebooks/offline_catalogs.html
# per costruirmi il mio dataset da zero e cercare di evitare i problemi di questo... soprattutto per quanto riguarda i sottogeneri
# se non ci sono info sul sottogenere, cerco di farli io "a mano" (a posteriori) con clustering basato sulle descrizioni
# ecc... 
# provare tutte le cose sopra


