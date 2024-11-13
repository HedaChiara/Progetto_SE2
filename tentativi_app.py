import streamlit as st
import polars as pl

data = pl.read_csv("sf_books_tidy.csv")

# Titolo
st.write("""
# Libri di Fantascienza
""")

# libri considerati migliori, per autore
st.write("""
## Quali sono le valutazioni dei libri di un certo autore?
""")
autori = data.select("Author_Name").unique().sort("Author_Name")

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

# ha qualcosa che non va... es: per Asimov, Nightfall ha barra più lunga ma punteggio minore di altre barre più corte
st.bar_chart(
     bar_valutazione_autore,
     x = "Book_Title",
     x_label = "Valutazione",
     y="Rating_score",
     y_label = "Titolo",
    horizontal=True
    )


# Autori più prolifici (metto i primi 25)

st.write("""
## Quali sono gli autori più prolifici?
""")

scatter_autori_nlibri = (
    data
    .group_by(pl.col("Author_Name"))
    .agg(
        pl.count("Book_Title")
         .alias("Book_Number")
    ).sort("Book_Number", descending = True)
)

# è un po' brutto, come migliorare?
st.scatter_chart(
    scatter_autori_nlibri.head(25),
    x = "Author_Name",
    x_label = "Autore",
    y = "Book_Number",
    y_label = "Numero di libri",
    size = "Book_Number",
    height = 500
)

# o meglio?
st.bar_chart(
    scatter_autori_nlibri.head(15),
    x = "Author_Name",
    x_label = "Autore",
    y = "Book_Number",
    y_label = "Numero di libri",
    horizontal = True
)

# Le valutazioni sono influenzate dall'anno di uscita? plot year vs rating score
# Il numero di valutazioni è influenzato dall'anno di uscita? 
# Qual è il genere più amato? (con migliori valutazioni) barplot genere vs rating score
# L'anno di pubblicazione influenza il genere di un libro? (anni in classi ampie 10 o 20 vs numero di libri per ogni genere)








