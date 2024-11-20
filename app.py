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
Le seguenti analisi si basano sui dati su libri di fantascienza scaricabili [qui]({url}), opportunamente ripuliti.
La procedura di preprocessing dei dati è documentata nell'Appendice A <- scoprire come mettere il riferimento
 """
         )


#### Libri considerati migliori, per autore ####
st.write("""
## Quali sono le valutazioni dei libri di un certo autore?
         
Il seguente grafico consente di selezionare un autore e visualizzare le valutazioni di ogni suo libro
""")

autori = data.select("Author_Name").unique().sort("Author_Name")
# selezione autore da parte dell'utente
autore_selezionato = st.selectbox(
    "Seleziona un autore",
    autori,
    index = None,
    placeholder = ""
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
## Quali sono i libri con valutazioni migliori di un dato genere?
         
Il seguente grafico consente di selezionare un sottogenere della fantascienza e visualizzare i libri meglio valutati.
""")

# selezione del numero di libri da visualizzare da parte dell'utente
n_libri = range(1, 101)
n_libri_selezionato = st.select_slider("Quanti libri vorresti visualizzare?", n_libri, value=20)

# selezione del genere da parte dell'utente
generi = ["Alieni", "Alternate History", "Universo Alternativo", "Apocalittico", "Cyberpunk", 
          "Distopia", "Fantascienza Hard", "Militare", "Robot", "Space Opera", "Steampunk", "Viaggi nel Tempo"]
genere_selezionato = st.selectbox(
    "Seleziona un genere",
    generi,
    index = 5,
    placeholder = "",
)
# grafici a barre dei libri migliori, in base al genere e al numero selezionati
diz_generi_indicatrici = {
    "Alieni" : "I_alien", "Alternate History" : "I_alt_hist", "Universo Alternativo" : "I_alt_uni", "Apocalittico" : "I_apo", 
    "Cyberpunk" : "I_cpunk", "Distopia" : "I_dyst", "Fantascienza Hard" : "I_hard", "Militare" : "I_mil", "Robot" : "I_robot", 
    "Space Opera" : "I_space", "Steampunk" : "I_steam", "Viaggi nel Tempo" : "I_ttravel"
}

bar_rating_genere = (
    alt.Chart(data.filter(pl.col(diz_generi_indicatrici[genere_selezionato]) == 1).sort(pl.col("Rating_score"), descending=True).head(n_libri_selezionato))
    .mark_bar()
    .encode(
        alt.Y("Book_Title", sort="-x", title="Titolo"),
        alt.X("Rating_score", title="Valutazione")
    )
    )

st.altair_chart(bar_rating_genere, use_container_width=True)
# Upgrade:    
# Farlo solo per i libri più famosi



#### Autori più prolifici (primi 15) ####
st.write("""
## Quali sono gli autori più prolifici?
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

# Upgrade:
# st.write("""
# ## Che genere di libri hanno scritto? E in che anni?
# """)

# Possibile upgrade: far vedere gli autori più prolifici per genere (è un casino raggruppare per genere, ho solo indicatrici)
# dovrei guardare, per ogni indicatrice di genere, quali righe hanno 1 in quella colonna e tenere traccia dell'autore (unique)


#### Anni in cui sono stati scritti più libri ####
st.write("""
## Quali sono gli anni in cui sono stati scritti più libri di fantascienza?
Il grafico seguente mostra l'andamento del numero di libri di fantascienza scritti nel corso degli anni dal 1900 al 2020
""")

# checkbox per far decidere se visualizzare anche grafico per libri molto valutazioni
# volendo posso mettere anche uno slidere per far decidere il numero di valutazioni
check_valutazioni = st.checkbox(
    "Visualizza l'andamento solo per libri con più di 750000 valutazioni",
    value = False
)

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
if check_valutazioni:
    st.line_chart(
        famous_books,
        x="Year_published",
        y="Book_Count"
)

st.write("""
Si nota un andamento tendenzialmente crescente del numero di libri di fantascienza scritti negli anni, in particolare è evidente 
una rapida ascesa negli anni seguenti il 2005 che culmina con un picco nel 2013.
Goodreads è stato lanciato nel 2007, per cui una spiegazione plausibile del trend osservato è che a seguito della sua creazione 
siano stati inseriti nel catalogo più libri poco famosi o di autori meno affermati rispetto a quanto fatto in passato. 
Un'ulteriore indicazione di ciò è che il picco del 2013 coincide con l'anno di acquisto di Goodreads da parte di Amazon, 
che aggiunge automaticamente i libri presenti nel proprio catalogo a quello di Goodreads. (?) 
Magari invece sono stati fattori sociali e tecnologici, ma che coincidenza... 
Si riscontra infine un notevole decremento del numero di libri scritti negli anni seguenti al 2013.
""")


st.write("""
## Quanti libri di fantascienza appartenenti ai vari sottogeneri sono stati scritti negli anni?
Il seguente grafico consente di selezionare uno o più sottogeneri e di visualizzare il numero di libri appartenenti
a quei sottogeneri scritti negli anni
""")





#### L'anno di pubblicazione influenza il genere di un libro? (anni in classi ampie circa 10 vs numero di libri per ogni genere) ####
# alcuni libri hanno anno di pubblicazione 0, li escludo
anni = [range(1900, 1970), range(1971, 1980), range(1981, 1990), range(1991, 2000), range(2001, 2010), range(2010, 2022)]







# Volendo posso importare immagini prese da grafici R ggplot... e in appendice metto come ho fatto a farlo



# Le valutazioni sono influenzate dall'anno di uscita? plot year vs rating score
# Il numero di valutazioni è influenzato dall'anno di uscita? 
# Qual è il genere più amato? (con migliori valutazioni) barplot genere vs rating score











