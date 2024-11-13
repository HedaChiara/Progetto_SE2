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



#### Libri con valutazione migliore, per genere (metto i primi 20) ####
st.write("""
## Quali sono i libri con valutazioni migliori di un dato genere?
""")

generi = ["Alieni", "Alternate History", "Universo Alternativo", "Apocalittico", "Cyberpunk", 
          "Distopia", "Fantascienza Hard", "Militare", "Robot", "Space Opera", "Steampunk", "Viaggi nel Tempo"]

# selezione dei generi da parte dell'utente
genere_selezionato = st.selectbox(
    "Seleziona un genere",
    generi,
    index = None,
    placeholder = ""
)
if(genere_selezionato == "Alieni"):
    bar_rating_genere = data.filter(pl.col("I_alien") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Alternate History"):
    bar_rating_genere = data.filter(pl.col("I_alt_hist") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Universo Alternativo"):
    bar_rating_genere = data.filter(pl.col("I_alt_uni") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Apocalittico"):
    bar_rating_genere = data.filter(pl.col("I_apo") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Cyberpunk"):
    bar_rating_genere = data.filter(pl.col("I_cpunk") == 1).sort("Rating_score", descending=True)
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Distopia"):
    bar_rating_genere = data.filter(pl.col("I_dyst") == 1).sort("Rating_score", descending=True)    
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Fantascienza Hard"):
    bar_rating_genere = data.filter(pl.col("I_hard") == 1).sort("Rating_score", descending=True)  
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Militare"):
    bar_rating_genere = data.filter(pl.col("I_mil") == 1).sort("Rating_score", descending=True)  
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Robot"):
    bar_rating_genere = data.filter(pl.col("I_robots") == 1).sort("Rating_score", descending=True)  
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Space Opera"):
    bar_rating_genere = data.filter(pl.col("I_space") == 1).sort("Rating_score", descending=True)  
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Steampunk"):
    bar_rating_genere = data.filter(pl.col("I_steam") == 1).sort("Rating_score", descending=True) 
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)
elif(genere_selezionato == "Viaggi nel Tempo"):
    bar_rating_genere = data.filter(pl.col("I_ttravel") == 1).sort("Rating_score", descending=True) 
    st.bar_chart(
    bar_rating_genere.head(20),
    x = "Book_Title",
    x_label = "Valutazione",
    y = "Rating_score",
    y_label = "Titolo",
    horizontal = True    
)




### Autori più prolifici (primi 15) ####
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
    y = "Book_Number",
    y_label = "Numero di libri",
    horizontal = True
)

# Possibile upgrade: far vedere gli autori più prolifici per genere (casino raggruppare per genere, ho solo indicatrici)





# Volendo posso importare immagini prese da grafici R ggplot... e in appendice metto come ho fatto a farlo



# Le valutazioni sono influenzate dall'anno di uscita? plot year vs rating score
# Il numero di valutazioni è influenzato dall'anno di uscita? 
# Qual è il genere più amato? (con migliori valutazioni) barplot genere vs rating score
# L'anno di pubblicazione influenza il genere di un libro? (anni in classi ampie 10 o 20 vs numero di libri per ogni genere)








