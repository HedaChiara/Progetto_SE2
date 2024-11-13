import streamlit as st
import polars as pl

data = pl.read_csv("sf_books_tidy.csv")

# Titolo
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



#### Autori più prolifici, per genere (metto i primi 25) ####
st.write("""
## Quali sono gli autori più prolifici?
""")

generi = ["Alieni", "Alternate History", "Universo alternativo", "Apocalittico", "Cyberpunk", 
          "Distopia", "Fantascienza Hard", "Militare", "Robot", "Space Opera", "Steampunk", "Viaggi nel Tempo"]
# selezione dei generi da parte dell'utente
generi_selezionati = st.multiselect(
    "Seleziona uno o più generi",
    generi,
    placeholder = "",
    # di default, mostra gli autori più prolifici in generale (per tutti i generi)
    default = generi
)

# dataframe con colonne Autore - Numero di libri scritti - Generi
autori_nlibri = (
    data
    .group_by(pl.col("Author_Name"))
    .agg(
        pl.count("Book_Title")
         .alias("Book_Number")
    ).sort("Book_Number", descending = True)
)

autori_nlibri.write_csv("Book_Count_by_Author.csv")



# grafico a barre
st.bar_chart(
    autori_nlibri.head(15),
    x = "Author_Name",
    x_label = "Autore",
    y = "Book_Number",
    y_label = "Numero di libri",
    horizontal = True
)
# Volendo posso importare immagine presa da grafico R ggplot... e in appendice metto come ho fatto a farlo



# Le valutazioni sono influenzate dall'anno di uscita? plot year vs rating score
# Il numero di valutazioni è influenzato dall'anno di uscita? 
# Qual è il genere più amato? (con migliori valutazioni) barplot genere vs rating score
# L'anno di pubblicazione influenza il genere di un libro? (anni in classi ampie 10 o 20 vs numero di libri per ogni genere)








