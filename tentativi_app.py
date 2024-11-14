import streamlit as st
import polars as pl

data = pl.read_csv("sf_books_tidy.csv")



#### Titolo ####
st.write("""
# Libri di Fantascienza
""")



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
    data
    .filter(pl.col("Author_Name") == autore_selezionato)
    .select(pl.col(["Book_Title", "Rating_score"]))
    .sort("Rating_score", descending=True)
)
# grafico a barre (si può ordinare?)
st.bar_chart(
     bar_valutazione_autore,
     x = "Book_Title",
     x_label = "Valutazione",
     y="Rating_score",
     y_label = "Titolo",
    horizontal=True
    )



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
    index = None,
    placeholder = ""
)
# grafici a barre dei libri migliori, in base al genere e al numero selezionati

# POSSO USARE .WHEN E .THEN MA INSERENDO NELLA CONDIZIONE SOLO UNA VARIABILE ESTERNA (genere_selezionato) 
# SE LO FACCIO MI DICE CHE NON E' DEFINITA

if(genere_selezionato == "Alieni"):
    bar_rating_genere = data.filter(pl.col("I_alien") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Alternate History"):
    bar_rating_genere = data.filter(pl.col("I_alt_hist") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Universo Alternativo"):
    bar_rating_genere = data.filter(pl.col("I_alt_uni") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Apocalittico"):
    bar_rating_genere = data.filter(pl.col("I_apo") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Cyberpunk"):
    bar_rating_genere = data.filter(pl.col("I_cpunk") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Distopia"):
    bar_rating_genere = data.filter(pl.col("I_dyst") == 1).sort("Rating_score", descending=True)    
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Fantascienza Hard"):
    bar_rating_genere = data.filter(pl.col("I_hard") == 1).sort("Rating_score", descending=True)  
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Militare"):
    bar_rating_genere = data.filter(pl.col("I_mil") == 1).sort("Rating_score", descending=True)  
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Robot"):
    bar_rating_genere = data.filter(pl.col("I_robots") == 1).sort("Rating_score", descending=True)  
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Space Opera"):
    bar_rating_genere = data.filter(pl.col("I_space") == 1).sort("Rating_score", descending=True)  
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Steampunk"):
    bar_rating_genere = data.filter(pl.col("I_steam") == 1).sort("Rating_score", descending=True) 
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Viaggi nel Tempo"):
    bar_rating_genere = data.filter(pl.col("I_ttravel") == 1).sort("Rating_score", descending=True) 
    st.bar_chart(
    bar_rating_genere.head(n_libri_selezionato),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
    
# Upgrade:    
# Posso mettere una selezione tipo quadratino on/off che fa scegliere all'utente se vuole vedere solo i libri 
# con più di un certo numero (fissato ad esempio a 1 milione) di valutazioni?




#### Autori più prolifici (primi 15) ####
st.write("""
## Quali sono gli autori più prolifici?
""")
# dataframe 
autori_nlibri = pl.read_csv("Book_Count_by_Author.csv")
# grafico a barre 
st.bar_chart(
    autori_nlibri.head(15),
    x = "Author_Name",
    x_label = "Autore",
    y = "Book_Count",
    y_label = "Numero di libri",
    horizontal = True
)

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
book_count_year = pl.read_csv("book_count_per_year.csv")
st.line_chart(
    book_count_year,
    x="Year_published",
    y="Book_Count"

)
st.write("""
Si nota un andamento tendenzialmente crescente del numero di libri di fantascienza scritti negli anni, in particolare si evidenzia 
una rapida ascesa negli anni seguenti il 2005 che culmina con un picco nel 2013.
Goodreads è stato lanciato nel 2007, per cui una spiegazione plausibile del trend osservato è che a seguito della sua creazione 
siano stati inseriti nel suo catalogo più libri poco famosi o di autori meno affermati rispetto a quanto fatto in passato. 
Un ulteriore fatto che porta a pensare a ciò, è che il picco del 2013 coincide con l'anno di acquisto di Goodreads da parte di Amazon, 
che aggiunge automaticamente i libri presenti nel proprio catalogo a quello di Goodreads. 
Si riscontra infine un notevole decremento del numero di libri scritti negli anni seguenti.

Segue un grafico che mostra l'andamento dei libri scritti negli anni, solamente per libri con più di 750000 valutazioni
""")
famous_books = pl.read_csv("famous_books.csv")
st.line_chart(
    famous_books,
    x="Year_published",
    y="Book_Count"
)


st.write("""
## Quanti libri di fantascienza appartenenti ai vari sottogeneri sono stati scritti negli anni?
Il seguente grafico consente di selezionare uno o più sottogeneri e di visualizzare il numero di libri appartenenti
a quei sottogeneri scritti negli anni
""")
book_count_year = pl.read_csv("book_count_per_year_per_genre.csv")




#### L'anno di pubblicazione influenza il genere di un libro? (anni in classi ampie circa 10 vs numero di libri per ogni genere) ####
# alcuni libri hanno anno di pubblicazione 0, li escludo
anni = [range(1900, 1970), range(1971, 1980), range(1981, 1990), range(1991, 2000), range(2001, 2010), range(2010, 2022)]






# Volendo posso importare immagini prese da grafici R ggplot... e in appendice metto come ho fatto a farlo



# Le valutazioni sono influenzate dall'anno di uscita? plot year vs rating score
# Il numero di valutazioni è influenzato dall'anno di uscita? 
# Qual è il genere più amato? (con migliori valutazioni) barplot genere vs rating score











