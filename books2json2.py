import polars as pl
import json

data = (pl.read_csv("sf_books_tidy.csv").filter(pl.col("Book_Description").is_not_null())
        .filter(pl.col("Author_Name").is_not_null())
        .filter(pl.col("Book_Title").is_not_null())
        .select(["Book_Title", "Author_Name", "Book_Description"])
)
descr_dict = (
    data.write_json()
)

# qui ho una lista di dizionari {titolo:"", autore:"", descrizione:""}
descr_dict = json.loads(descr_dict)

# faccio un dizionario unico {"titolo, autore" : descrizione}
better_descr_dict = {}
for d in descr_dict:
    # definisco la chiave come tupla di titolo e autore (univoca) e come valore la sua descrizione
    better_descr_dict[str(d["Book_Title"] + ", " + d["Author_Name"])] = d["Book_Description"]

# N.B. avrei preferito avere una tupla (titolo, autore) come chiave, ma json.dump non lo permette
# in caso posso crearmelo dopo... almeno così le chiavi sono univoche.

with open("sf_books2.json", "w") as f:
    json.dump(better_descr_dict, f)


