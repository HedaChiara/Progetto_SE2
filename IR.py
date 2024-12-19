import streamlit as st
import polars as pl
import json

@st.cache_data
def get_data(path):
    data = pl.read_csv(path)
    return data
# aggiungo degli identificatori numerici di riga con .with_row_count
data = get_data("sf_books_tidy.csv").drop_nulls(pl.col("Book_Description")).with_row_index("id")
st.write(data)

st.write("""
## Reperimento di libri
""")
# mi serve un file .json strutturato così: {BOOK : {BOOK_ID : ..., TITLE : ...,  AUTHOR : ..., DESCRIPTION : ... }}, {...}, ...
books = (
    data.write_json()
)
books_json = json.loads(books)
with open("IR_books.json", "w") as f:
    json.dump(books_json, f)


