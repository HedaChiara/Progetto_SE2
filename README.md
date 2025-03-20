## I dati
Lo scopo del progetto è l'analisi di questo [dataframe di libri di fantascienza](https://www.kaggle.com/datasets/tanguypledel/science-fiction-books-subgenres) 
contenente dati ricavati da Goodreads su circa 11000 libri.
## Le analisi
Dopo aver opportunamente preprocessato i dati, ho implementato un'applicazione web usando Streamlit in modo da esporre chiaramente i grafici e i risultati ottenuti.  
L'analisi si focalizza in prima battuta sulle valutazioni date dagli utenti di Goodreads. Vengono inoltre forniti dei tool per visualizzare i libri meglio valutati a partire da un certo autore oppure
da un sottogenere della fantascienza, con la possibilità di limitare la ricerca ai soli libri "famosi".  
Seguono poi dei confronti tra l'andamento del numero di libri usciti negli anni e quello per i soli libri che hanno avuto successo. Un confronto analogo è stato fatto tra i libri ed i film di fantascienza.  
Vengono infine mostrati una wordcloud delle parole che appaiono più frequentemente nelle descrizioni dei libri e un recommender system che usando [doc2vec](https://radimrehurek.com/gensim/models/doc2vec.html)
consiglia i 10 libri più simili a quello dato in input dall'utente.
## Sviluppi futuri
Miglioramenti del recommender system.
## Esecuzione
Per eseguire l'applicazione, è sufficiente scaricare i file di questa repository e digitare "uv run streamlit run app.py" da terminale.  
In alternativa, si può accedere direttamente all'app tramite il link https://sciencefictionbooks.streamlit.app/.
