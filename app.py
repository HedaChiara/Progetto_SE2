import streamlit as st
import polars as pl
import altair as alt

# per esegurire, uv run streamlit run app.py

data = pl.read_csv("sf_books_tidy.csv")

url = "https://www.kaggle.com/datasets/tanguypledel/science-fiction-books-subgenres"

#### Titolo ####
st.write("""
# Libri di Fantascienza
""")

st.write(
f"""
Le seguenti analisi si basano su dati riguardanti libri di fantascienza estratti da [Goodreads]({"https://www.goodreads.com/"}) e scaricabili [qui]({url}), opportunamente preprocessati.
La procedura di pulizia dei dati è documentata nell'Appendice A, in fondo alla pagina.  

 """
         )

## ANALISI SUI RATING SCORE
st.write("""
## Analisi riguardanti le valutazioni dei libri
""")

#### Libri considerati migliori, per autore ####
st.write("""
### Quali sono le valutazioni dei libri di un certo autore?
         
Il seguente grafico consente di selezionare un autore e visualizzare le valutazioni di ogni suo libro.  
Le valutazioni vanno da un minimo di 0 ad un massimo di 5
""")

autori = data.select("Author_Name").unique().sort("Author_Name")
# selezione autore da parte dell'utente
autore_selezionato = st.selectbox(
    "Seleziona un autore",
    autori,
    index = 3021,
    placeholder = "",

)
bar_valutazione_autore = (
    alt.Chart(data.filter(pl.col("Author_Name") == autore_selezionato).select(pl.col(["Book_Title", "Rating_score"])))
    .mark_bar()
    .encode(
        alt.X("Rating_score"),
        alt.Y("Book_Title", sort="-x"),
    )
    #.sort("Rating_score", descending=True)
)
# grafico a barre
st.altair_chart(bar_valutazione_autore, use_container_width=True)



#### Libri con valutazione migliore, per genere ####
st.write("""
### Quali sono i libri con valutazioni migliori di un dato genere?
         
Il seguente grafico consente di selezionare un sottogenere della fantascienza e visualizzare i libri meglio valutati, con la possibilità
di escludere quelli meno famosi (quelli con meno di 750000 valutazioni).
""")

# selezione del genere da parte dell'utente
generi = ["Alieni", "Alternate History", "Universo Alternativo", "Apocalittico", "Cyberpunk", 
          "Distopia", "Fantascienza Hard", "Militare", "Robot", "Space Opera", "Steampunk", "Viaggi nel Tempo"]
diz_generi_indicatrici = {
    "Alieni" : "I_alien", "Alternate History" : "I_alt_hist", "Universo Alternativo" : "I_alt_uni", "Apocalittico" : "I_apo", 
    "Cyberpunk" : "I_cpunk", "Distopia" : "I_dyst", "Fantascienza Hard" : "I_hard", "Militare" : "I_mil", "Robot" : "I_robots", 
    "Space Opera" : "I_space", "Steampunk" : "I_steam", "Viaggi nel Tempo" : "I_ttravel"
}
genere_selezionato = st.selectbox(
    "Seleziona un genere",
    generi,
    index = 5,
    placeholder = "",
)

# selezione del numero di libri da visualizzare da parte dell'utente
n_libri = range(1, 201)
n_libri_selezionato = st.select_slider("Quanti libri vorresti visualizzare, al massimo?", n_libri, value=20)

check_valutazioni1 = st.checkbox(
    f"Mostra solo i libri di questo sottogenere con più di 750000 valutazioni",
    value = False
)

# grafici a barre dei libri migliori, in base al genere e al numero selezionati
bar_rating_genere = (
    alt.Chart(data.filter(pl.col(diz_generi_indicatrici[genere_selezionato]) == 1).sort(pl.col("Rating_score"), descending=True).head(n_libri_selezionato))
    .mark_bar()
    .encode(
        alt.Y("Book_Title", sort="-x", title="Titolo"),
        alt.X("Rating_score", title="Valutazione")
    )
    )

bar_rating_genere_famosi = (
    alt.Chart(data.filter(pl.col(diz_generi_indicatrici[genere_selezionato]) == 1).filter(pl.col("Rating_votes") >= 750000).sort(pl.col("Rating_score"), descending=True).head(n_libri_selezionato))
    .mark_bar()
    .encode(
        alt.Y("Book_Title", sort="-x", title="Titolo"),
        alt.X("Rating_score", title="Valutazione")
    )
    )

if not check_valutazioni1:
    st.altair_chart(bar_rating_genere, use_container_width=True)
else:
    st.altair_chart(bar_rating_genere_famosi, use_container_width=True)


#### Grafico a torta delle valutazioni (tra 1 e 3, tra 3 e 4, tra 4 e 5) -> gli utenti di Goodreads sono generosi? ####
st.write('''
### Che valutazioni vengono date ai libri?
''')
# raggruppo le valutazioni in 4 classi
classi_valutazioni = {"Scadente" : [0, 3.5], "Mediocre" : [3.5, 4], "Buono" : [4, 4.5], "Eccellente" : [4.5, 5]}
# aggiungo una colonna in cui ho la classe di valutazione a cui appartiene il libro
data = data.with_columns(
    Rating_score_class =
    pl.when(pl.col("Rating_score") >= classi_valutazioni["Scadente"][0], pl.col("Rating_score") < classi_valutazioni["Scadente"][1] ).then(pl.lit("Scadente (tra 0 e 3.5)"))
    .when(pl.col("Rating_score") >= classi_valutazioni["Mediocre"][0], pl.col("Rating_score") < classi_valutazioni["Mediocre"][1] ).then(pl.lit("Mediocre (tra 3.5 e 4)"))
    .when(pl.col("Rating_score") >= classi_valutazioni["Buono"][0], pl.col("Rating_score") < classi_valutazioni["Buono"][1] ).then(pl.lit("Buono (tra 4 e 4.5)"))
    .when(pl.col("Rating_score") >= classi_valutazioni["Eccellente"][0], pl.col("Rating_score") < classi_valutazioni["Eccellente"][1] ).then(pl.lit("Eccellente (tra 4.5 e 5)"))
    .alias("Rating_score_class")
)
# st.write(media_valutazioni = data.select("Rating_score").mean())

check_valutazioni2 = st.checkbox(
    f"Mostra solo le valutazioni dei libri con più di mezzo milione di valutazioni",
    value = False
)

# COME CAMBIO L'ORDINE DELLE CATEGORIE NELLA LEGENDA?

# grafico a torta delle valutazioni
pie_valutazioni = (
    alt.Chart(data.drop_nulls("Rating_score_class"))
    .mark_arc(radius=70, radius2=130, cornerRadius=15)
    .encode(
        alt.Theta("Rating_score_class", aggregate="count"),
        alt.Color("Rating_score_class", sort=["Scadente", "Mediocre", "Buono", "Eccellente"]).scale(scheme="category10").legend(title="Valutazione"),
        
    )
)
# percentuali per ogni classe
percentuali_valutazioni = data.group_by("Rating_score_class").agg()
pie_valutazioni_text = (
    alt.Chart(percentuali_valutazioni)
    .mark_text(radius=120)
    .encode(
        alt.Text("", aggregate="count"),
        alt.Theta("pop", aggregate="sum"),
        alt.Color("continent")
    )

)

# solo per i libri più famosi
pie_valutazioni_famosi =(
    alt.Chart(data.drop_nulls("Rating_score_class").filter(pl.col("Rating_votes") >= 500000))
    .mark_arc(radius=70, radius2=130, cornerRadius=15)
    .encode(
        alt.Theta("Rating_score_class", aggregate="count"),
        alt.Color("Rating_score_class", sort=["Scadente", "Mediocre", "Buono", "Eccellente"]).scale(scheme="category10").legend(title="Valutazione", ),
        
    )
)
# testo con le percentuali
pie_valutazioni_famosi_text = (

)

if check_valutazioni2:
    st.altair_chart(pie_valutazioni_famosi + pie_valutazioni_text, use_container_width=True)
else:
    st.altair_chart(pie_valutazioni + pie_valutazioni_famosi_text, use_container_width=True)

st.write('''
Gli utenti di Goodreads hanno valutato come mediocre o buona la qualità della maggior parte dei libri di fantascienza nel catalogo.  
Guardando solamente le valutazioni dei libri più famosi, scompare la categoria "Scadente" ed aumenta invece la proporzione di libri valutati come buoni ed eccellenti.  
''')







# Qual è il genere più amato? (con migliori valutazioni) barplot genere vs rating score




## ANALISI SUL NUMERO DI LIBRI SCRITTI NEGLI ANNI
st.write("""
## Analisi sul numero di libri scritti negli anni
""")

#### Autori più prolifici (primi 15) ####
st.write("""
### Quali sono gli autori più prolifici?
""")
# dataframe 
autori_nlibri = pl.read_csv("Book_Count_by_Author.csv")
# grafico a barre 
bar_autori_prolifici = (
    alt.Chart(autori_nlibri.head(15))
    .mark_bar()
    .encode(
        alt.Y("Author_Name", title="Autore", sort="-x"),
        alt.X("Book_Count", title="Numero di libri scritti")
    )
)
st.altair_chart(bar_autori_prolifici, use_container_width=True)

# Upgrade: far vedere gli autori più prolifici per genere (è un casino raggruppare per genere, ho solo indicatrici)
# dovrei guardare, per ogni indicatrice di genere, quali righe hanno 1 in quella colonna e tenere traccia dell'autore (unique)

# st.write("""
# ## Che genere di libri hanno scritto? E in che anni?
# """)




#### Anni in cui sono stati scritti più libri ####
st.write("""
### Quali sono gli anni in cui sono stati scritti più libri di fantascienza?
Il grafico seguente mostra l'andamento del numero di libri di fantascienza scritti nel corso degli anni dal 1900 al 2020
""")

# checkbox per far decidere se visualizzare anche grafico per libri molto valutati
# volendo posso mettere anche uno slider per far decidere il numero di valutazioni
n_valutazioni = st.number_input(label="Inserisci qui il numero minimo di valutazioni che un libro deve avere per essere mostrato",min_value=0, max_value=5000000, label_visibility="visible")

check_valutazioni2 = st.checkbox(
    f"Visualizza anche l'andamento per i libri con più di {n_valutazioni} valutazioni",
    value = False
)

# LAYER ALTAIR ...

book_count_year = pl.read_csv("book_count_per_year.csv")
st.line_chart(
    book_count_year,
    x="Year_published",
    x_label = "Anno di Pubblicazione",
    y="Book_Count",
    y_label = "Numero di libri scritti"
)

famous_books = pl.read_csv("famous_books.csv")
# posso farlo con Altair (aggiungere grafico a grafico già esistente)
if check_valutazioni2:
    st.line_chart(
        famous_books,
        x="Year_published",
        y="Book_Count"
)

# mettere anche checkbox per vedere solo andamento dei libri con recensioni > della media delle valutazioni

st.write("""
Si nota un andamento tendenzialmente crescente del numero di libri di fantascienza scritti nel corso del tempo, in particolare è evidente 
una rapida ascesa negli anni successivi al 2005 che culmina con un picco nel 2013.  
Probabilmente questo rapido aumento è dovuto all'evoluzione e alla diffusione della tecnologia e al boom dell'editoria digitale che ha permesso a chiunque
di scrivere e pubblicare libri molto più facilmente rispetto al passato.  
E' curioso notare che Goodreads è stato lanciato nel 2007 e che Amazon, che aggiunge i libri presenti nel proprio catalogo
a quello di Goodreads in modo automatico, l'ha acquistato proprio nel 2013, anno in cui si è registrato il picco di libri scritti.  
Si riscontra infine un notevole decremento del numero di libri scritti dopo il 2013.
""")


st.write("""
### Quanti libri di fantascienza appartenenti ai vari sottogeneri sono stati scritti negli anni?
Il seguente grafico consente di selezionare uno o più sottogeneri e di visualizzare il numero di libri appartenenti
a quei sottogeneri scritti negli anni
""")

# LAYERS 




#### L'anno di pubblicazione influenza il genere di un libro? (anni in classi ampie circa 10 vs numero di libri per ogni genere) ####
# alcuni libri hanno anno di pubblicazione 0, li escludo
anni = [range(1900, 1970), range(1971, 1980), range(1981, 1990), range(1991, 2000), range(2001, 2010), range(2010, 2022)]






# Le valutazioni sono influenzate dall'anno di uscita? plot year vs rating score
# Il numero di valutazioni è influenzato dall'anno di uscita? 





#### RECOMMENDATION SYSTEM - INSERISCO UN LIBRO CHE MI PIACE E ME NE SUGGERISCE ALTRI (potrei inserire dei filtri)
# Idee: 
# - PRIMO APPROCCIO: dopo un opportuno preprocessing delle descrizioni (eliminazione delle stop word, tokenizzazione, stemming)
# posso usare word2vec e poi trovo i libri più simili a quello dato usando una metrica di similarità tipo la cosine similarity o la distanza euclidea
# - COSA PIU' STRUTTURATA: faccio clustering tenendo conto anche dei generi e dell'autore (se dello stesso autore, aumenta la similarità)
# - MIGLIORAMENTI: ampliare le descrizioni esistenti aggiungendo altro

#### SCRIVO UNA PAROLA (o una frase) E MI DICE QUALI LIBRI PARLANO DI QUESTA COSA (magari faccio vedere solo i migliori)



# APPENDICE A - PREPROCESSING DEI DATI
with st.expander(label = "Appendice A", expanded=False, icon=None):
    st.write('''
    Spiegazione della pulizia:  
    Blah blah blah
    ''')
    # scrivere una breve spiegazione
    # rimandare a Tidying.py
    pass







