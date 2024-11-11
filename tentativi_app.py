import streamlit as st
import polars as pl

data = pl.read_csv("sf_books_tidy.csv")

st.write("""
# Libri di Fantascienza
""")

# libri considerati migliori, per autore
st.write("""
## Quali sono i libri con valutazione migliore di un dato autore?
""")
autori = data.select("Author_Name").unique().sort("Author_Name")
autore_selezionato = st.multiselect(
    "Seleziona un autore",
    autori
)

bar_valutazione_autore = (
    data
    .filter(pl.col("Author_Name") == autore_selezionato)
    .sort("Rating_score")
    .with_columns(
        pl.col("Book_Title").cast(pl.Categorical())
    )
    .sort("Rating_score")
)

st.bar_chart(
    bar_valutazione_autore,
    x="Book_Title",
    y="Rating_score",
    horizontal=True
)












