import polars as pl

# Dataframe dei 12 sottogeneri (N.B. un libro può appartenere a più di uno di questi dataframe)
alien = pl.read_csv("sf_aliens.csv")
alt_hist = pl.read_csv("sf_alternate_history.csv")
alt_uni = pl.read_csv("sf_alternate_universe.csv")
apo = pl.read_csv("sf_apocalyptic.csv")
cpunk = pl.read_csv("sf_cyberpunk.csv")
dyst = pl.read_csv("sf_dystopia.csv")
hard = pl.read_csv("sf_hard.csv")
mil = pl.read_csv("sf_military.csv")
robots = pl.read_csv("sf_robots.csv")
space = pl.read_csv("sf_space_opera.csv")
steam = pl.read_csv("sf_steampunk.csv")
ttravel = pl.read_csv("sf_time_travel.csv")

# Dataframe risultante dalla concatenazione dei precedenti dataframe (14974, 11)
books = pl.concat([alien, alt_hist, alt_uni, apo, cpunk, dyst, hard, mil, robots, space, steam, ttravel])
books.write_csv("concat_books.csv")

# La variabile Genres non va bene: è un dizionario {genere : numero_persone_che_hanno_votato_quel_genere} e ha al suo interno delle chiavi
# che non sono nemmeno generi (es. "audiobook", "40k")
# La elimino dal dataframe e al suo posto inserisco 12 variabili indicatrici corrispondenti ai 12 sottogeneri che identificavano 
# i precedenti dataframe. 
# Ogni libro avrà un 1 nella colonna del k-esimo genere se apparteneva al k-esimo dataframe dei generi e 0 in tutte le altre
# Problema: ci saranno dei doppioni (i libri che appartengono a più di uno dei 12 precedenti dataframe)

# Inizializzo queste variabili come vettori di 14974 zeri
n = books.shape[0]
I_alien = [0] * n
I_alt_hist = [0] * n
I_alt_uni = [0] * n
I_apo = [0] * n
I_cpunk = [0] * n
I_dyst = [0] * n
I_hard = [0] * n
I_mil = [0] * n
I_robots = [0] * n
I_space = [0] * n
I_steam = [0] * n
I_ttravel = [0] * n
# Titoli delle indicatrici del genere
new_columns = [I_alien, I_alt_hist, I_alt_uni, I_apo, I_cpunk, I_dyst, I_hard, I_mil, I_robots, I_space, I_steam, I_ttravel]
# Lista dei dataframe dei generi
genres = [alien, alt_hist, alt_uni, apo, cpunk, dyst, hard, mil, robots, space, steam, ttravel]
# Lista delle lunghezze di ogni dataframe dei generi
len_genres = [genre.shape[0] for genre in genres]
# Inserisco gli 1 nelle indicatrici dei generi (seguo l'ordine iniziale: i primi alien.shape[0] libri avranno 1 su I_alien e 0 sul resto, 
# e così via, fino ad avere tutti 0 e ttravel.shape[0] 1 per gli ultimi libri (appartenenti a ttravel))
# k è il numero di riga iniziale dei dataframe dei generi, la inizializzo a 0 per i libri appartenenti ad alien
k = 0
for i in range(0, len(new_columns)):
    # metto 1 al posto di 0 nelle posizioni da k a k + numero di libri appartenenti al genere corrente
    new_columns[i][k : k + len_genres[i]] = [1] * len_genres[i]
    # aggiorno k aggiungendo il numero di libri appartenenti al genere corrente
    k += len_genres[i]

# Elimino le colonne Genres, Original_Book_Title, che non sono utili ai fini delle analisi
books = books.drop(["Genres", "Original_Book_Title"])
# Aggiungo le 12 Indicatrici di genere
books = books.with_columns([pl.Series(name="I_alien", values=I_alien),
                            pl.Series(name="I_alt_hist", values=I_alt_hist),
                            pl.Series(name="I_alt_uni", values=I_alt_uni),
                            pl.Series(name="I_apo", values=I_apo),
                            pl.Series(name="I_cpunk", values=I_cpunk),
                            pl.Series(name="I_dyst", values=I_dyst),
                            pl.Series(name="I_hard", values=I_hard),
                            pl.Series(name="I_mil", values=I_mil),
                            pl.Series(name="I_robots", values=I_robots),
                            pl.Series(name="I_space", values=I_space),
                            pl.Series(name="I_steam", values=I_steam),
                            pl.Series(name="I_ttravel", values=I_ttravel)
                            ])

# Mi assicuro che le variabili abbiano come valori stringhe senza spazi iniziali e finali
books = books.with_columns(
    pl.col("url").str.strip_chars(),
    pl.col("Book_Title").str.strip_chars(),
    pl.col("Author_Name").str.strip_chars(),
    pl.col("Book_Description").str.strip_chars()
    )          
                
# Elimino i libri che compaiono più volte con la stessa url (e sommo le indicatrici dei generi)
no_duplicates = books.group_by(["Book_Title", "Author_Name", "Edition_Language", "Rating_score", "Rating_votes", "Review_number", "Book_Description", "Year_published", "url"]
                       ).agg([pl.col(["I_alien", "I_alt_hist", "I_alt_uni", "I_apo", "I_cpunk", "I_dyst", "I_hard", "I_mil", "I_robots", "I_space", "I_steam", "I_ttravel"])
                       .sum()])

# I doppioni però non sono stati del tutto eliminati:                      
# ci sono alcune discrepanze nei dati, ad es: il libro "11/22/63" ha un numero di Rating_score diverso in righe differenti.
# Lo stesso vale per Rating_Votes e tanti altri libri.
# Ciò probabilmente significa che i dati sullo stesso libro sono stati raccolti in momenti diversi, 
# quindi nel frattempo sono state raccolte nuove valutazioni, scritte nuove recensioni e il Rating_score è stato modificato. 

# Soluzione: per ogni libro, se ci sono discrepanze, prendo come valore di Review_number il massimo tra i valori osservati 
# (cioè il dato più recente), e faccio lo stesso per Rating_votes.
# Come valore di Rating_score dovrei prendere quello dell'osservazione con il valore di Rating_votes più alto (sempre il dato più recente)
# Attenzione: sui duplicati rimasti, non essendo stati raggruppati insieme, vanno ancora sommate le indicatrici, come fatto sopra

# Problema: alcuni libri che sono duplicati, hanno url diverse. Nuovo criterio di uguaglianza per questi libri: stesso titolo e autore.
# dataframe di 4 colonne in cui metto i dati più recenti
dati_recenti = (
    no_duplicates.sort(
        by = "Rating_votes", descending=True)
        .unique(
            ["Book_Title", "Author_Name"],  keep = "first", maintain_order = True)
        .select(["Book_Title","Author_Name","Rating_score", "Book_Description"])
)

# Elimino i duplicati (ordino i libri secondo "Rating_votes" in modo da avere come primi i dati più recenti)
no_duplicates = (
    # elimino i libri che non sono editi in inglese (pochi e con tanti dati mancanti)
    no_duplicates.filter(pl.col("Edition_Language").is_in(["English", "None"]))
    .sort(by = "Rating_votes", descending=True).group_by(
    ["Book_Title", "Author_Name"]
    ).agg(
        pl.col("Rating_votes").max(),
        pl.col("Review_number").max(),
        # Il libro "Starship Troopers" ha un problema: in righe diverse risultano anni di pubblicazione diversi (quello vero è il minore)"
        pl.col("Year_published").min(), 
        # Sommo le indicatrici dei generi
        pl.col(["I_alien", "I_alt_hist", "I_alt_uni", "I_apo", "I_cpunk", "I_dyst", "I_hard", "I_mil", "I_robots", "I_space", "I_steam", "I_ttravel"])
        .sum()
        # aggiungo i dati più recenti
        ).join(dati_recenti, on = ["Book_Title", "Author_Name"], how = "inner")
)
# Ho tolto la colonna url in quanto non informativa

# file .csv senza libri duplicati (tidy)
no_duplicates.write_csv("sf_books_tidy.csv")