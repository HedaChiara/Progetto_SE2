import streamlit as st
import polars as pl
import altair as alt  # mi serve per avere grafici ordinati secondo ciò che voglio io, non secondo l'ordine alfabetico delle x

data = pl.read_csv("sf_books_tidy.csv")

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

st.bar_chart(
     bar_valutazione_autore,
     x = "Book_Title",
     x_label = "Titolo",
     y="Rating_score",
     y_label = "Valutazione",
    horizontal=True
    )












