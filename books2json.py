import polars as pl
import json

data = pl.read_csv("sf_books_tidy.csv").filter(pl.col("Book_Description").is_not_null()).select(["Book_Title", "Author_Name", "Book_Description"])

# io vorrei un dizionario (titolo, autore):"descrizione"
# così ho {
#     "titolo1" : [
#         0 : {
#             "Book_Title" : "titolo1"
#             "Author_Name" : "..."
#             "Book_Description" : "..."
#         }
#          1 : {
#             "Book_Title" : "titolo1"
#             "Author_Name" : "..."
#             "Book_Description" : "..."
#         }
#          ...
#     ]
# }
# se sono più libri con stesso titolo, ho due dizionari all'interno del dizionario con chiave "titolo", con chiavi 0, 1, 2, ...
# I guess it's ok
descr_dict = (
    data.rows_by_key(key = "Book_Title", include_key=True, named=True)
    # data.rows_by_key(key = ["Book_Title","Author_Name"], include_key=True, named=True, unique=True)
    # non funziona, mi dice che la chiave non può essere una tupla, ma nella documentazione fanno proprio così...
)
descr_dict

with open("sf_books.json", "w") as f:
    json.dump(descr_dict, f)






# da Book_Description, rimuovere tutti gli "alternative cover", "ISBN ...", ""




