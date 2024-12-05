import streamlit as st
import polars as pl
import altair as alt

# per eseguire, uv run streamlit run app.py
# mettere un po' di @st.cache_data
@st.cache_data
def get_data(path):
    data = pl.read_csv(path)
    return data

data = get_data("sf_books_tidy.csv")

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

#### Grafico a torta delle valutazioni (tra 1 e 3, tra 3 e 4, tra 4 e 5) -> gli utenti di Goodreads sono generosi? ####
st.write('''
### Come si distribuiscono le valutazioni date ai libri?
''')
# raggruppo le valutazioni in 4 classi
classi_valutazioni = {"Scadente" : [0, 3.5], "Mediocre" : [3.5, 4], "Buono" : [4, 4.5], "Eccellente" : [4.5, 5]}
# aggiungo una colonna in cui ho la classe di valutazione a cui appartiene il libro
data = data.with_columns(
    Rating_score_class =
    pl.when(pl.col("Rating_score") >= classi_valutazioni["Scadente"][0], pl.col("Rating_score") < classi_valutazioni["Scadente"][1] ).then(pl.lit("0 - 3.5: Scadente"))
    .when(pl.col("Rating_score") >= classi_valutazioni["Mediocre"][0], pl.col("Rating_score") < classi_valutazioni["Mediocre"][1] ).then(pl.lit("3.5 - 4: Mediocre"))
    .when(pl.col("Rating_score") >= classi_valutazioni["Buono"][0], pl.col("Rating_score") < classi_valutazioni["Buono"][1] ).then(pl.lit("4 - 4.5: Buono"))
    .when(pl.col("Rating_score") >= classi_valutazioni["Eccellente"][0], pl.col("Rating_score") < classi_valutazioni["Eccellente"][1] ).then(pl.lit("4.5 - 5: Eccellente"))
    .alias("Rating_score_class")
)
# st.write(media_valutazioni = data.select("Rating_score").mean())
check_valutazioni2 = st.checkbox(
    f"Mostra solo le valutazioni dei libri con più di mezzo milione di valutazioni",
    value = False
)
# grafico a torta delle valutazioni
pie_valutazioni = (
    alt.Chart(data.drop_nulls("Rating_score_class"))
    .mark_arc(radius=70, radius2=130, cornerRadius=20)
    .encode(
        alt.Theta("Rating_score_class", aggregate="count"),
        alt.Color("Rating_score_class").scale(range=["orangered", "orange", "deepskyblue", "yellowgreen"]).legend(title="Valutazione")
    )
)
# testo con le percentuali
text_valutazioni = (
    pie_valutazioni
    .mark_text(radius=160, size=20)
    .transform_aggregate(count_books = "count(Book_Title)", groupby=["Rating_score_class"])
    .transform_calculate(percentage = "round(datum.count_books / 11091 * 100) + '%'")
    .encode(
        alt.Text("percentage:N"),
        alt.Theta("count_books:Q").stack(True),
    )
)
# grafico a torta solo per i libri più famosi
pie_valutazioni_famosi =(
    alt.Chart(data.drop_nulls("Rating_score_class").filter(pl.col("Rating_votes") >= 500000))
    .mark_arc(radius=70, radius2=130, cornerRadius=15)
    .encode(
        alt.Theta("Rating_score_class", aggregate="count"),
        alt.Color("Rating_score_class").scale(range=["orange", "deepskyblue", "yellowgreen"]).legend(title="Valutazione"),
        
    )
)
# st.write(data.drop_nulls("Rating_score_class").filter(pl.col("Rating_votes") >= 500000).shape[0])
# st.write(data.drop_nulls("Rating_score_class").filter(pl.col("Rating_votes") >= 500000).select(pl.col("Rating_score")).mean())
# testo con le percentuali solo per i libri più famosi
text_valutazioni_famosi = (
    pie_valutazioni_famosi
    .mark_text(radius=160, size=20, align="center")
    .transform_aggregate(count_books = "count(Book_Title)", groupby=["Rating_score_class"])
    .transform_calculate(percentage = "round(datum.count_books / 95 * 100) + '%'")
    .encode(
        alt.Text("percentage:N"),
        alt.Theta("count_books:Q").stack(True)
    )
)
if not check_valutazioni2:
    st.altair_chart(pie_valutazioni + text_valutazioni, use_container_width=True)
else:
    st.altair_chart(pie_valutazioni_famosi + text_valutazioni_famosi, use_container_width=True)
st.write('''
Gli utenti di Goodreads hanno valutato come mediocre o buona la qualità della maggior parte dei libri di fantascienza nel catalogo. La valutazione media è 3.92.  
Guardando solamente le valutazioni dei libri più famosi, scompare la categoria "Scadente" ed aumenta invece la percentuale di libri valutati come buoni ed eccellenti.
La valutazione media per questi libri sale a 4.14.
''')
# Qual è il genere più amato? (con migliori valutazioni) pie chart genere vs rating score per ogni genere
# un po' complicato visto che un libro appartiene a più di un genere


#### Libri con valutazione migliore, per genere ####
st.write("""
### Quali sono i libri con valutazioni migliori di un dato sottogenere della fantascienza?
         
Il seguente grafico consente di selezionare un sottogenere della fantascienza e visualizzare i libri meglio valutati, con la possibilità
di escludere quelli meno famosi (quelli con meno di 250000 valutazioni).
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
n_libri = range(1, 101)
n_libri_selezionato = st.select_slider("Quanti libri vorresti visualizzare, al massimo?", n_libri, value=10)

check_valutazioni1 = st.checkbox(
    f"Mostra solo i libri di questo sottogenere con più di 250000 valutazioni",
    value = False
)

# grafici a barre dei libri migliori, in base al genere e al numero selezionati
bar_rating_genere = (
    alt.Chart(data.filter(pl.col(diz_generi_indicatrici[genere_selezionato]) == 1).sort(pl.col("Rating_score"), descending=True).head(n_libri_selezionato))
    .mark_bar()
    .encode(
        alt.Y("Book_Title", sort="-x", title="Titolo"),
        alt.X("Rating_score", title="Valutazione"),
        tooltip = [alt.Tooltip("Rating_score", title = "Valutazione"),
        alt.Tooltip("Book_Title", title = "Titolo"),
        alt.Tooltip("Author_Name", title = "Autore")]
    )
    )

bar_rating_genere_famosi = (
    alt.Chart(data.filter(pl.col(diz_generi_indicatrici[genere_selezionato]) == 1).filter(pl.col("Rating_votes") >= 250000).sort(pl.col("Rating_score"), descending=True).head(n_libri_selezionato))
    .mark_bar()
    .encode(
        alt.Y("Book_Title", sort="-x", title="Titolo"),
        alt.X("Rating_score", title="Valutazione"),
        tooltip = [alt.Tooltip("Rating_score", title = "Valutazione"),
        alt.Tooltip("Book_Title", title = "Titolo"),
        alt.Tooltip("Author_Name", title = "Autore")]   
        )
    )

if not check_valutazioni1:
    st.altair_chart(bar_rating_genere, use_container_width=True)
else:
    st.altair_chart(bar_rating_genere_famosi, use_container_width=True)



#### Le valutazioni sono influenzate dall'anno di uscita? ####
st.write('''
### La qualità dei libri pubblicati è rimasta costante negli anni?  
Il seguente grafico mostra la variabilità nella qualità (intesa come media delle valutazioni degli utenti di Goodreads) dei libri pubblicati nei quinquenni
dal 1961 al 2020. In nero la media delle valutazioni su tutti gli anni.
''')
# boxplot di Rating_score per intervalli di 5 anni dal 1961 al 2020 (ne vengono fuori troppi se faccio per ogni anno)
box_valutazioni_anni = (
    alt.Chart(data.filter(pl.col("Year_published") >= 1961).filter(pl.col("Year_published") <= 2020).filter(pl.col("Rating_score")>0))
    # colonna con quinquennio nella forma "anno_inizio-anno_fine"
    .transform_calculate(five_years_period = "floor((datum.Year_published-1961)/5)*5+1961 + '-' + (floor((datum.Year_published-1961)/5)*5+1965)")
    .mark_boxplot()
    .encode(
        alt.Y("Rating_score:Q", title = "Valutazione").scale(domain=[2,5]),
        alt.X("five_years_period:N", title = "Quinquennio", axis=alt.Axis(labelAngle=-45)),
        # quando passo su un outlier, vedo titolo, autore e anno di pubblicazione
        tooltip = [alt.Tooltip("Rating_score", title = "Valutazione"),
        alt.Tooltip("Book_Title", title = "Titolo"),
        alt.Tooltip("Author_Name", title = "Autore"),
        alt.Tooltip("Year_published", title = "Anno di pubblicazione")] 
    )
)
# media per i libri pubblicati dopo il 1960 (rimane 3.92 come quella generale)
line_media_valutazioni = (
    alt.Chart(pl.DataFrame({"media":[3.92]}))
    .mark_rule()
    .encode(
        alt.Y("media").scale(domain=[2,5]),
        alt.Color(value="black")
    )
)
st.altair_chart((box_valutazioni_anni + line_media_valutazioni), use_container_width=True)
st.write('''
Non si notano grosse differenze nella qualità dei libri scritti nel corso degli anni, se non nel numero di outliers, che è aumentato 
in particolar modo per i libri scritti negli ultimi 10 anni, i quali presentano anche una variabilità nella qualità lievemente maggiore rispetto ai libri meno recenti.   
Si può notare come le mediane delle valutazioni stiano tendenzialmente sotto alla media generale:
sono quindi stati scritti più libri con valutazione sotto la media che sopra la media.  
E' curioso notare che il quinquennio con valutazione mediana peggiore sia il primo (1961-1965) e quello con valutazione mediana maggiore sia l'ultimo (2016-2020).  
Gli utenti di Goodreads sembrano quindi preferire libri più recenti. 
''')
# sarebbe carino evidenziare con un'area colorata il cambiamento nella varianza


#### Libri considerati migliori, per autore ####
st.write("""
### Quali sono i libri migliori di un certo autore?
         
Il seguente grafico consente di selezionare un autore e visualizzare le valutazioni di ogni suo libro.
""")
# lista degli autori
autori = data.select("Author_Name").unique().sort("Author_Name")
# selezione autore da parte dell'utente
autore_selezionato = st.selectbox(
    "Seleziona un autore",
    autori,
    index = 3021,
    placeholder = "",

)
# grafico a barre dei libri dell'autore selezionato, ordinati dal migliore al peggiore
bar_valutazione_autore = (
    alt.Chart(data.filter(pl.col("Author_Name") == autore_selezionato).select(pl.col(["Book_Title", "Rating_score"])))
    .mark_bar()
    .encode(
        alt.X("Rating_score", title="Valutazione"),
        alt.Y("Book_Title", title="Titolo", sort="-x"),
    )
)
st.altair_chart(bar_valutazione_autore, use_container_width=True)
# aggiungere slider per il numero di valutazioni diventa troppo?





## ANALISI SUL NUMERO DI LIBRI SCRITTI NEGLI ANNI
st.write("""
## Analisi sul numero di libri scritti negli anni
""")

#### Autori più prolifici (primi 15) ####
st.write("""
### Quali sono gli autori più prolifici?
""")
# dataframe 
autori_nlibri = (
    data
    .group_by(pl.col("Author_Name"))
    .agg(
        pl.count("Book_Title")
         .alias("Book_Count")
    ).sort("Book_Count", descending = True)
)
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

# in media quanti libri scrive un autore?

# Upgrade: far vedere gli autori più prolifici per genere (è un casino raggruppare per genere, ho solo indicatrici)
# dovrei guardare, per ogni indicatrice di genere, quali righe hanno 1 in quella colonna e tenere traccia dell'autore (unique)

# st.write("""
# ## Che genere di libri hanno scritto? E in che anni?
# """)


# vedere dati film

#### Anni in cui sono stati scritti più libri ####
st.write("""
### Quali sono gli anni in cui sono stati scritti più libri di fantascienza?
Il grafico seguente mostra l'andamento del numero di libri di fantascienza scritti nel corso degli anni dal 1920 al 2020
""")

# checkbox per far decidere se visualizzare anche grafico per libri molto valutati
# slider numero di valutazioni
n_valutazioni = st.slider(label="Inserisci il numero minimo di valutazioni che un libro deve avere per essere mostrato",
min_value=0, max_value=250000, step=50000, label_visibility="visible", value=100000)
# checkbox mostra solo libri famosi
check_valutazioni2 = st.checkbox(
    f"Visualizza anche l'andamento per i libri con più di {n_valutazioni} valutazioni",
    value = True
)
# grafico numero_libri vs anno per tutti i libri
line_libri_anno = (
    alt.Chart(data.group_by(pl.col("Year_published")).agg(pl.count("Book_Title").alias("Book_Count"))
              .filter(pl.col("Year_published") >= 1920, pl.col("Year_published")< 2021))
    .mark_line()
    .encode(
        alt.X("Year_published", title="Anno di Pubblicazione"),
        alt.Y("Book_Count", title="Numero di Libri")
    ) 
)
# grafico numero_libri vs anno per i soli libri con più di n_valutazioni valutazioni
line_libri_famosi_anno = (
    alt.Chart(data.filter(pl.col("Rating_votes") >= n_valutazioni).group_by(pl.col("Year_published")).agg(pl.count("Book_Title").alias("Book_Count"))
              .filter(pl.col("Year_published") >= 1920, pl.col("Year_published")< 2021))
    .mark_line()
    .encode(
        alt.X("Year_published", title="Anno di Pubblicazione"),
        alt.Y("Book_Count", title="Numero di Libri Famosi"),
        alt.Color(value = "orange")
    )
)
if not check_valutazioni2:
   st.altair_chart(line_libri_anno, use_container_width=True)
else:
    st.altair_chart((line_libri_anno + line_libri_famosi_anno).resolve_scale(y='independent'), use_container_width=True)


st.write("""
Si nota un andamento tendenzialmente crescente del numero di libri di fantascienza scritti nel corso del tempo, in particolare è evidente 
una rapida ascesa negli anni successivi al 2005 che culmina con un picco nel 2013.  
Probabilmente questo rapido aumento è dovuto all'evoluzione e alla diffusione della tecnologia e al boom dell'editoria digitale che ha permesso a chiunque
di scrivere e pubblicare libri molto più facilmente rispetto al passato.  
E' curioso notare che Goodreads è stato lanciato nel 2007 e che Amazon, che aggiunge i libri presenti nel proprio catalogo
a quello di Goodreads in modo automatico, l'ha acquistato proprio nel 2013, anno in cui si è registrato il picco di libri scritti.  
Si riscontra infine un notevole decremento del numero di libri scritti dopo il 2013.  
E' interessante notare come nell'anno in cui sono stati pubblicati più libri in assoluto, in proporzione abbia avuto successo una minima parte di essi:
ad esempio tra gli 893 libri usciti nel 2013, ce ne sono solamente 18 con più di 100000 valutazioni.
Al contrario, il 2011 sembra essere l'anno in cui più libri hanno avuto successo (proporzionatamente al numero di libri pubblicati in quell'anno)
""")
# st.write(data.filter(pl.col("Year_published") == 2011).filter(pl.col("Rating_votes")>100000).select("Book_Title"))





#### RECOMMENDATION SYSTEM - INSERISCO UN LIBRO CHE MI PIACE E ME NE SUGGERISCE ALTRI (potrei inserire dei filtri)
# Idee: 
# - PRIMO APPROCCIO: dopo un opportuno preprocessing delle descrizioni (eliminazione delle stop word, tokenizzazione, stemming)
# posso usare word2vec e poi trovo i libri più simili a quello dato usando una metrica di similarità tipo la cosine similarity o la distanza euclidea
# - COSA PIU' STRUTTURATA: faccio clustering tenendo conto anche dei generi e dell'autore (se dello stesso autore, aumenta la similarità)
# - MIGLIORAMENTI: ampliare le descrizioni esistenti aggiungendo altro
# Documento i vari tentativi e scelgo il migliore (come?)

#### SCRIVO UNA PAROLA (o una frase) E MI DICE QUALI LIBRI PARLANO DI QUESTA COSA (magari faccio vedere solo i migliori)
# Information retrieval con Elasticsearch, ho praticamente già tutto fatto e posso anche usare il mio miglioramento
# Scrivo un po' di giudizi di rilevanza a mano e via!



# APPENDICE A - PREPROCESSING DEI DATI
with st.expander(label = "Appendice A", expanded=False, icon=None):
    st.write('''
    Inizialmente c'erano 12 dataset contenenti i libri appartenenti a sottogeneri diversi della fantascienza,
    quindi ho deciso di unirli tutti in un unico dataframe
             
    Spiegazione della pulizia:  
    Blah blah blah

    Per scaricare il file .py con il codice di preprocessing commentato dettagliatamente, clicca sotto
    (devo ancora scoprire come fare)
    ''')
    # mi sa che devo trasformare i miei file in oggetti Bytes
    st.download_button(label="Download dataframe", data = "Capisci come mettere file")
    st.download_button(label="Download preprocessing", data = "Capisci come mettere file")
    # scrivere una breve spiegazione
    # rimandare a Tidying.py







