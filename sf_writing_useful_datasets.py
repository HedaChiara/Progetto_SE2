import polars as pl

data = pl.read_csv("sf_books_tidy.csv")

# dataframe con colonne Autore - Book_Count per autore
autori_nlibri = (
    data
    .group_by(pl.col("Author_Name"))
    .agg(
        pl.count("Book_Title")
         .alias("Book_Count")
    ).sort("Book_Count", descending = True)
)
autori_nlibri.write_csv("Book_Count_by_Author.csv")


# dataframe con colonne Year_published - Book_Count per anno di pubblicazione
# tolgo quelli che hanno anno di pubblicazione < 1900 (ce ne sono alcuni che hanno valore 0)
book_year = (
    data
    .group_by(pl.col("Year_published"))
    .agg(
        pl.count("Book_Title")
        .alias("Book_Count")
    ).filter(pl.col("Year_published") >= 1900, pl.col("Year_published")< 2021)
    .sort("Book_Count", descending=True)
)
book_year.write_csv("book_count_per_year.csv")

# dataframe con colonne Titolo - Anno - N° Valutazioni
famous_books = (
    data
    .filter(pl.col("Rating_votes") > 750000)
    .group_by(pl.col(["Year_published"]))
    .agg(pl.count("Book_Title")
        .alias("Book_Count"))
 )

famous_books.write_csv("famous_books.csv")
