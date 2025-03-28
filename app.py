import streamlit as st
import polars as pl
import altair as alt
import json
import wordcloud
import matplotlib.pyplot as plt
import gensim

# per eseguire, uv run streamlit run app.py da terminale

# carico i dati
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
    .transform_calculate(percentage = "round(datum.count_books / 10951 * 100) + '%'")
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

# checkbox per la visualizzazione dei soli libri famosi
check_valutazioni1 = st.checkbox(
    f"Mostra solo i libri di questo sottogenere con più di 250000 valutazioni",
    value = False
)

# grafici a barre dei libri meglio valutati, in base al genere e al numero selezionati
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
# strip plot della valutazione dei libri per ogni quinquennio
circle_valutazioni_anni = (
    alt.Chart(data.filter(pl.col("Year_published") >= 1961).filter(pl.col("Year_published") <= 2020).filter(pl.col("Rating_score")>0))
    .transform_calculate(five_years_period = "floor((datum.Year_published-1961)/5)*5+1961 + '-' + (floor((datum.Year_published-1961)/5)*5+1965)")
    .mark_circle(size=5, opacity=0.4)
    .encode(
        alt.Y("Rating_score:Q", title = "Valutazione").scale(domain=[2,5]),
        alt.X("five_years_period:N", title = "Quinquennio", axis=alt.Axis(labelAngle=-45)),
        alt.XOffset("jitter:Q"),
        alt.Color(value="darkorange"),
        tooltip = [alt.Tooltip("Rating_score", title = "Valutazione"),
        alt.Tooltip("Book_Title", title = "Titolo"),
        alt.Tooltip("Author_Name", title = "Autore"),
        alt.Tooltip("Year_published", title = "Anno di pubblicazione")]
    ).transform_calculate(
    # jitter gaussiano con trasformazione di Box-Muller
    jitter="sqrt(-2*log(random()))*cos(2*PI*random())"
    )   
)

# boxplot di Rating_score per intervalli di 5 anni dal 1961 al 2020
box_valutazioni_anni = (
    alt.Chart(data.filter(pl.col("Year_published") >= 1961).filter(pl.col("Year_published") <= 2020).filter(pl.col("Rating_score")>0))
    # colonna con quinquennio nella forma "anno_inizio-anno_fine"
    .transform_calculate(five_years_period = "floor((datum.Year_published-1961)/5)*5+1961 + '-' + (floor((datum.Year_published-1961)/5)*5+1965)")
    # non mostro gli outlier (già mostrati nel layer sotto)
    .mark_boxplot(outliers={'size': 0})
    .encode(
        alt.Y("Rating_score:Q", title = "Valutazione").scale(domain=[2,5]),
        alt.X("five_years_period:N", title = "Quinquennio", axis=alt.Axis(labelAngle=-45))
    )
)
# media per i libri pubblicati dopo il 1960 (rimane 3.92 come quella generale)
line_media_valutazioni = (
    alt.Chart(pl.DataFrame({"media":[3.92]}))
    .mark_rule(size=1.5)
    .encode(
        alt.Y("media").scale(domain=[2,5]),
        alt.Color(value="black")
    )
)

st.altair_chart((circle_valutazioni_anni + box_valutazioni_anni + line_media_valutazioni).resolve_scale(yOffset='independent'), use_container_width=True)
st.write('''
Non si notano differenze nette nella qualità dei libri scritti nel corso degli anni, se non nel numero di outliers, che è aumentato 
in particolar modo per i libri scritti negli ultimi 10 anni, i quali presentano una variabilità nella qualità maggiore rispetto ai libri meno recenti.  
Si può notare come le mediane delle valutazioni stiano tendenzialmente sotto alla media generale:
sono quindi stati scritti più libri con valutazione sotto la media che sopra la media.  
E' curioso notare che il quinquennio con valutazione mediana peggiore sia il primo (1961-1965) e quello con valutazione mediana maggiore sia l'ultimo (2016-2020).  
Gli utenti di Goodreads sembrano quindi avere una preferenza per i libri più recenti.  
Molto diverso è invece il numero di libri scritti negli anni, che aumenta sempre più col passare del tempo.
''')

st.write('''
Il grafico seguente è simile a quello sopra, con la differenza che si può apprezzare la variazione del numero di libri scritti in un 
certo anno (non quinquennio) con una certa valutazione in base al colore.  
In particolare, si riscontra un notevole aumento del numero di libri dopo gli anni '90 (settori colorati più intensamente secondo la scala)
e anche della variabilità nelle valutazioni, infatti si nota che negli ultimi anni sono stati pubblicati libri valutati molto sopra la media ma anche molto sotto.
''')

# heatmap
heat_valutazione_anni = (
    alt.Chart(data.filter(pl.col("Year_published") >= 1950).filter(pl.col("Year_published") <= 2020).filter(pl.col("Rating_score")>0))
    .properties(
        height = 350
    )
    .mark_rect()
    .encode(
        alt.X("Year_published:O", title="Anno di pubblicazione", axis=alt.Axis(labelAngle=-45)),
        alt.Y("Rating_score:O", title="Valutazione", sort="descending"),
        alt.Color("Book_Title", aggregate="count").scale(scheme="viridis").legend(title="N° libri")
    )
)
st.altair_chart(heat_valutazione_anni, use_container_width=True)

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
    index = 2988,
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



## ANALISI SUL NUMERO DI LIBRI SCRITTI NEGLI ANNI
st.write("""
## Analisi riguardanti il numero di libri scritti negli anni
""")

#### Autori più prolifici (primi 15) ####
# in media quanti libri di fantascienza scrive un autore?
# st.write(autori_nlibri.select(pl.col("Book_Count")).mean())
st.write("""
### Quali sono gli autori più prolifici?
Il seguente grafico mostra gli autori che hanno scritto più libri di fantascienza
(da notare che il numero medio di libri scritti da un autore è circa 2.8)
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

# # istogramma numero libri scritti
# bar_numero_libri = (
#     alt.Chart(autori_nlibri)
#     .mark_bar()
#     .encode(
#         alt.X("Book_Count").bin(maxbins=40),
#         alt.Y("count()")
#     )
# )
# st.altair_chart(bar_numero_libri, use_container_width=True)
# tantissimi autori hanno scritto pochi libri (non lo mostro in quanto non è un grafico gradevole)


#### Anni in cui sono stati scritti più libri ####
st.write("""
### Quali sono gli anni in cui sono stati scritti più libri di fantascienza?
Il grafico seguente mostra l'andamento del numero di libri di fantascienza scritti nel corso degli anni dal 1950 al 2020 (in blu) e
l'andamento del numero di libri di fantascienza scritti nel corso degli anni che hanno un numero minimo a scelta di valutazioni (in arancione).  
N.B. le due scale sono naturalmente diverse.
""")

# slider numero di valutazioni
n_valutazioni = st.slider(label="Inserisci il numero minimo di valutazioni che un libro deve avere per essere mostrato",
min_value=50000, max_value=250000, step=50000, label_visibility="visible", value=100000)
# checkbox per mostrare solo libri famosi
check_valutazioni2 = st.checkbox(
    f"Visualizza anche l'andamento per i libri con più di {n_valutazioni} valutazioni",
    value = True
)
# grafico numero_libri vs anno per tutti i libri
line_libri_anno = (
    alt.Chart(data.group_by(pl.col("Year_published")).agg(pl.count("Book_Title").alias("Book_Count"))
              .filter(pl.col("Year_published") >= 1950, pl.col("Year_published")< 2021))
    .mark_line()
    .encode(
        alt.X("Year_published:O", title="Anno di Pubblicazione",  axis=alt.Axis(labelAngle=-45)),
        alt.Y("Book_Count", title="Numero di Libri")
    ) 
)
# grafico numero_libri vs anno per i soli libri con più di n_valutazioni valutazioni
line_libri_famosi_anno = (
    alt.Chart(data.filter(pl.col("Rating_votes") >= n_valutazioni).group_by(pl.col("Year_published")).agg(pl.count("Book_Title").alias("Book_Count"))
              .filter(pl.col("Year_published") >= 1950, pl.col("Year_published") < 2021))
    .mark_line()
    .encode(
        alt.X("Year_published:O", title="Anno di Pubblicazione",  axis=alt.Axis(labelAngle=-45)),
        alt.Y("Book_Count", title="Numero di Libri Famosi"),
        alt.Color(value = "orange")
    )
)
if not check_valutazioni2:
   st.altair_chart(line_libri_anno, use_container_width=True)
else:
    # titolo del grafico
    st.markdown('<div style="text-align: center;"><span style="color: #0068c9; font-size: 24px;">Libri</span> <span style="font-size: 24px;">vs</span> <span style="color: orange; font-size: 24px;">libri famosi</span></div>', unsafe_allow_html=True)
    st.altair_chart((line_libri_anno + line_libri_famosi_anno).resolve_scale(y='independent'), use_container_width=True)

st.write("""
Come si è potuto vedere anche dai grafici precedenti, si nota un andamento tendenzialmente crescente del numero di libri di fantascienza scritti nel corso del tempo, 
in particolare si riscontra una rapida ascesa negli anni successivi al 2005 che culmina con un picco nel 2013.  
Probabilmente questo aumento è dovuto inizialmente alla diffusione e all'evoluzione della tecnologia e al boom dell'editoria digitale poi, la quale ha permesso a chiunque
di scrivere e pubblicare libri molto più facilmente rispetto al passato.  
E' curioso notare che Goodreads è stato lanciato nel 2007 e che Amazon, che aggiunge i libri presenti nel proprio catalogo
a quello di Goodreads in modo automatico, l'ha acquistato nel 2013, anno in cui si è registrato il picco di libri scritti.  
Si riscontra infine un notevole decremento del numero di libri scritti dopo il 2013, forse a causa della difficoltà nella 
creazione di contenuti originali dopo così tanti anni zeppi di idee innovative, oltre che dal sempre maggiore interesse del pubblico 
(specialmente giovane) verso film e serie tv, che potrebbero aver soppiantato i libri come passatempo preferito.  
L'andamento del numero di libri famosi scritti ricalca abbastanza bene l'andamento generale ma risulta molto più irregolare. 
E' inoltre interessante notare come nell'anno in cui sono stati pubblicati più libri in assoluto, abbia avuto successo una minima parte di essi:
ad esempio tra gli 893 libri usciti nel 2013, ce ne sono solamente 18 con più di 100000 valutazioni.
Al contrario, il 2011 sembra essere l'anno in cui più libri hanno avuto successo (proporzionatamente al numero di libri pubblicati in quell'anno)
""")
# st.write(data.filter(pl.col("Year_published") == 2011).filter(pl.col("Rating_votes")>100000).select("Book_Title"))

#### Dati dei libri appaiati ai dati dei film (seguono lo stesso andamento?) ####
st.write('''
### L'andamento dei film segue quello dei libri?
Il grafico seguente mostra il numero di libri e di [film](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) di fantascienza usciti negli anni.  
Per maggiori informazioni sul dataframe, si veda l'appendice B in fondo alla pagina.
         ''')
# carico il dataframe dei film
movies = get_data("movies.csv")
# line chart del numero di film usciti negli anni
line_movies = (
    alt.Chart(movies.filter(pl.col("year")<=2017, pl.col("year")>=1950))
    .mark_line()
    .encode(
        alt.X("year:O", title="Anno di Pubblicazione",  axis=alt.Axis(labelAngle=-45)),
        alt.Y("title", aggregate="count", title="Numero di film usciti"),
        alt.Color(value="orange")
    )
)
# titolo del grafico
st.markdown('<div style="text-align: center;"><span style="color: #0068c9; font-size: 24px;">Libri</span> <span style="font-size: 24px;">vs</span> <span style="color: orange; font-size: 24px;">film</span></div>', unsafe_allow_html=True)
st.altair_chart((line_libri_anno + line_movies).resolve_scale(y="independent", color="independent"), use_container_width=True)
st.write('''
Da questo grafico si può notare come i due andamenti siano abbastanza simili, per quanto i dati sui film presentino irregolarità più marcate.  
L'aumento del numero di film usciti che inizia verso gli anni '80 potrebbe essere dovuto ad un maggiore interesse del pubblico verso questo 
genere, dopo il grande successo di alcuni film cult come Star Wars (1977), Alien (1979) e Blade Runner (1982), per poi esplodere sempre più 
in seguito a Matrix (1999) e Minority Report (2002), oltre al notevole salto di qualità nella realisticità degli effetti speciali.
Inoltre, sembra che l'industria cinematografica abbia in qualche modo risentito della crisi del 2008 (al contrario dell'editoria),
ma trattandosi questi di dati solamente su film di fantascienza, il calo nel numero di film usciti registrato dal 2009 al 2012 potrebbe 
essere indice di uno spostamento nei temi oltre che di una diminuzione del numero di film prodotti: 
ad esempio, alcuni produttori potrebbero aver preferito puntare su film più commerciali e quindi sicuri dal punto di vista del guadagno 
piuttosto che su film di fantascienza, pur avendo questi ultimi un seguito non indifferente.  
Come per i libri però, negli ultimi anni anche per i film si è assistito ad un drastico calo nei numeri, 
che accade in questo caso in concomitanza con il boom dei servizi di streaming.
         ''')
 

## ANALISI SULLE DESCRIZIONI 
st.write("""
## Analisi sulle descrizioni dei libri
""")
# carico il file di testo con tutte le descrizioni concatenate
@st.cache_data
def get_desc():
    with open("descriptions.txt", "r", encoding="utf-8") as f:
        desc = f.read()
    return desc
desc = get_desc()
st.write('''
### Quali sono le parole che appaiono più frequentemente nelle descrizioni dei libri?
Nella seguente immagine la dimensione delle parole mostrate è proporzionale alla loro frequenza.  
Per i dettagli, si veda l'appendice C in fondo alla pagina.
         ''')
# wordcloud delle parole presenti nelle descrizioni dei libri (stop word escluse)    
# fonte: https://amueller.github.io/word_cloud/auto_examples/simple.html#sphx-glr-auto-examples-simple-py
@st.cache_data
def get_wordcloud():
    return wordcloud.WordCloud(background_color="white").generate(desc)
wc = get_wordcloud()
plt.imshow(wc, interpolation='bilinear')
# nessun asse
plt.axis("off")
# ottimizza il posizionamento delle parole
plt.tight_layout()
# mostro l'immagine
st.pyplot(plt.gcf())
st.write('''
Le parole più frequenti sono naturalmente affiliate all'universo fantascientifico: da questa wordcloud si può infatti notare 
come vengano esplorati a fondo i temi di mondi e forme di vita differenti, guerre, battaglie e storie ambientate in altre epoche.
''')

## Recommender system
st.write('''
### Recommender System
         
Il tool seguente consente di inserire il titolo di un libro e di visualizzare i 10 libri più simili secondo il metodo 
[doc2vec](https://radimrehurek.com/gensim/models/doc2vec.html), basato sulle descrizioni dei libri. 
''')
# carico il dizionario con le descrizioni dei libri stemmate
def get_json(filename):
    with open (filename, "r") as f:
        data = json.load(f)
    return data
stemmed_descr = get_json("stemmed_descr.json")
# trasformo il dizionario in dataframe polars
book_descr_df = pl.DataFrame({
    "Book": stemmed_descr.keys(),
    "Description": stemmed_descr.values()
})
# selezione del libro da parte dell'utente
libro_selezionato = st.selectbox(
    "Seleziona un libro",
    book_descr_df.select("Book"),
    index = 2
)
# Modello con doc2vec
# fonti:
# https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.Doc2Vec
# https://stackoverflow.com/questions/42781292/doc2vec-get-most-similar-documents
@st.cache_data
def d2v():
    docs = []
    for book in stemmed_descr.keys():
        docs.append(gensim.models.doc2vec.TaggedDocument(words=stemmed_descr[book], tags=[book]))
    # modello
    model = gensim.models.doc2vec.Doc2Vec(docs, epochs=10)
    return model
model = d2v()



@st.cache_data
def recommend(selected_book, _model):
    # vettore del libro selezionato
    book_vec = model.infer_vector(stemmed_descr[selected_book])
    # salvo gli 11 libri più simili al libro selezionato (il primo sarà il libro selezionato stesso, quindi per mostrare la top ten ne salvo 11)
    top10 = model.docvecs.most_similar(positive=[book_vec], topn=11)
    # estraggo solamente i titoli
    titles = []
    for i in range(len(top10)):
        titles.append(top10[i][0])
    # dataframe con questi 10 titoli
    top10_df = pl.DataFrame({
    "Libri consigliati": titles[1:]
    })
    st.write(top10_df)

recommend(libro_selezionato, model)

st.write('''
N.B. Non sono stati effettuati dei test sulla bontà di questo recommender system, che è solamente una prima prova all'interno di un 
progetto molto più ampio che ha come obiettivo quello di testare diversi recommender system per capire quale è il migliore.
         ''')


#### Appendici ####
st.write('''
## Appendici
''')

# dataframe iniziale (da mettere nel download button alla fine)
initial_csv = get_data("concat_books.csv").serialize(format="binary")

# APPENDICE A - PREPROCESSING DEI DATI SUI LIBRI
with st.expander(label = "Appendice A - Data Preprocessing", expanded=False, icon=None):
    st.write('''
    I 12 dataset originali contenenti i libri appartenenti a sottogeneri diversi della fantascienza sono stati uniti in un unico dataframe,
    contenente però molti duplicati, visto che ogni libro può appartenere a diversi sottogeneri contemporaneamente. Una complicazione
    è stata data dal fatto che i dati sui libri nei 12 dataframe originali presentassero valori discordanti per alcune variabili
    e siano stati quindi probabilmente raccolti in momenti diversi. Nel dataframe su cui sono state effettuate le analisi
    sono stati tenuti solamente i dati più recenti e le variabili d'interesse.
             
    Per scaricare i dataframe originali (concatenati in un unico dataframe) ed il file .py con il codice di preprocessing
    commentato dettagliatamente, clicca sotto
    ''')
    
    st.download_button(label="Download dataframe", data = initial_csv, file_name="books.csv", mime="text/csv")
    with open("Tidying.py") as code:
        st.download_button('Download preprocessing', data = code, file_name="preprocessing_books.py")
    

# APPENDICE B - PREPROCESSING DEI DATI SUI FILM
binary_movies = movies.serialize(format="binary")
with st.expander(label = "Appendice B - Dati sui film", expanded=False, icon=None):
    st.write('''
    Il dataframe di film originale conteneva film di ogni genere e molte più informazioni di quelle necessarie per gli scopi
    di questa analisi. Sono perciò stati estratti solamente i dati rilevanti, ossia i soli titoli di film di fantascienza con le date di uscita.
             
    Per scaricare il dataframe originale ed il file .py con il codice di preprocessing, clicca sotto
    ''')
    
    st.download_button(label="Download dataframe", data = binary_movies, file_name="movies.csv", mime="text/csv")
    with open("Tidy_movies.py") as code:
        st.download_button('Download preprocessing', data = code, file_name="preprocessing_movies.py")
    

# APPENDICE C - PREPROCESSING DELLE DESCRIZIONI DEI LIBRI
with st.expander(label = "Appendice C - Preprocessing dei testi delle descrizioni", expanded=False, icon=None):
    st.write('''
    Per estrapolare le parole più frequenti presenti nelle descrizioni dei libri, ho effettuato una pulizia preliminare
    dei testi eliminando stop word, punteggiatura e parole poco interessanti come codici ISBN o link a siti web.  
    Per l'implementazione del recommender system è stato inoltre effettuato lo stemming delle parole nelle descrizioni dei libri.
                    
    Per scaricare il file .py con il codice di preprocessing, clicca sotto
    ''')
    with open("text_mining.py") as code:
        st.download_button('Download preprocessing', data = code, file_name="preprocessing_descriptions.py")