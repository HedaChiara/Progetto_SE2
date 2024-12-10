import polars as pl

movies = (
    pl.read_csv("movies_metadata.csv", has_header=True, ignore_errors=False, columns=["title", "genres", "release_date"], )
)

# mi interessano solo i film di fantascienza, che in questo dataset sono codificati con {'id': 878, 'name': 'Science Fiction'}
# all'interno della lista "genres" (che in realtà è una stringa del tipo "[{...}, {...}, ...]")
movies = movies.filter(pl.col("genres").str.contains("{'id': 878, 'name': 'Science Fiction'}", literal=True))

# elimino le variabili "genres" e "release_date", mantenendo solamente il titolo e l'anno di uscita come valore di "year"
movies = (movies.drop_nulls(pl.col("release_date"))
        .with_columns(
           [ pl.col("release_date").str.slice(0,4).cast(pl.Int64).alias("year"),
            pl.col("title").cast(pl.String) ]
            )
        .select(pl.col(["title", "year"]))
)

print(movies)

movies.write_csv("movies.csv")






