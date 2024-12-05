import streamlit as st
import polars as pl
import altair as alt
import nltk

data = pl.read_csv("sf_books_tidy.csv").select(["Book_Title", "Author_Name", "Book_Description"])

tokenized = (
    data.select(pl.col("Book_Description"))
)











