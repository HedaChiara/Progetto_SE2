setwd("C:/Users/chiar/OneDrive/Desktop/Uni/1_Statistica/15_Sistemi2/Progetto/ScienceFictionBooks")

library(tidyverse)

alien <- read.csv("sf_aliens.csv")
alt_hist <- read.csv("sf_alternate_history.csv")
alt_uni <- read.csv("sf_alternate_universe.csv")
apo <- read.csv("sf_apocalyptic.csv")
cpunk <- read.csv("sf_cyberpunk.csv")
dyst <- read.csv("sf_dystopia.csv")
hard <- read.csv("sf_hard.csv")
mil <- read.csv("sf_military.csv")
robots <- read.csv("sf_robots.csv")
space <- read.csv("sf_space_opera.csv")
steam <- read.csv("sf_steampunk.csv")
ttravel <- read.csv("sf_time_travel.csv")

# la variabile Genres va modificata per avere dei tidy data

# qui ho tutti di fila, ma ci sono tanti duplicati per via dei generi
data <- rbind(alien, alt_hist, alt_uni, apo, cpunk, dyst, hard, mil, robots, space, steam, ttravel)
dim(data)
View(data)

#### VARIABILI INDICATRICI DEI GENERI ####

n <- dim(data)[1]

I_alien <- c(rep(1, dim(alien)[1]), rep(0, n - dim(alien)[1])) # 1 se libro appartiene a genere alien, 0 altrimenti
I_alt_hist <- c(rep(0, dim(alien)[1]), rep(1, dim(alt_hist)[1]), rep(0, n - dim(alien)[1] - dim(alt_hist)[1]))
I_alt_uni <- c(rep(0, dim(alien)[1] + dim(alt_hist)[1]), rep(1, dim(alt_uni)[1]), rep(0, n - dim(alien)[1] - dim(alt_hist)[1] - dim(alt_uni)[1]))
k <- dim(alien)[1] + dim(alt_hist)[1] + dim(alt_uni)[1]
I_apo <- c(rep(0, k), rep(1, dim(apo)[1]), rep(0, n - k - dim(apo)[1]))
k <- k + dim(cpunk)[1]
I_cpunk <- c(rep(0, k), rep(1, dim(cpunk)[1]), rep(0, n - k - dim(cpunk)[1]))
k <- k + dim(dyst)[1]
I_dyst <- c(rep(0, k), rep(1, dim(dyst)[1]), rep(0, n - k - dim(dyst)[1]))
k <- k + dim(hard)[1]
I_hard <- c(rep(0, k), rep(1, dim(hard)[1]), rep(0, n - k - dim(hard)[1]))
k <- k + dim(mil)[1]
I_mil <- c(rep(0, k), rep(1, dim(mil)[1]), rep(0, n - k - dim(mil)[1]))
k <- k + dim(robots)[1]
I_robots <- c(rep(0, k), rep(1, dim(robots)[1]), rep(0, n - k - dim(robots)[1]))
k <- k + dim(space)[1]
I_space <- c(rep(0, k), rep(1, dim(space)[1]), rep(0, n - k - dim(space)[1]))
k <- k + dim(steam)[1]
I_steam <- c(rep(0, k), rep(1, dim(steam)[1]), rep(0, n - k - dim(steam)[1]))
k <- k + dim(ttravel)[1]
I_ttravel <- c(rep(0, k), rep(1, dim(ttravel)[1]), rep(0, n - k - dim(ttravel)[1]))

data <- mutate(data, I_alien, I_alt_hist, I_alt_uni, I_apo, I_cpunk, I_dyst, I_hard, I_mil, I_robots, I_space, I_steam, I_ttravel)
# Rimuovo la variabile Genres
data <- select(data, -Genres)


#### DATASET COMPLETO, con doppioni ####
write_excel_csv(data, "sf_books.csv")
books <- read_csv("sf_books.csv")
View(books) 

dupbooks <- read_csv("sf_books_with_duplicates.csv") 
View(dupbooks)

# devo ordinare secondo url
books <- books %>% arrange(url, .by_group = TRUE)
books <- books %>% select(-Original_Book_Title)
View(books)
table(books$Edition_Language) # poco interessante
View(books[,books$Edition_Language == "German"])

#### TIDY ####
t_books <- read_csv("sf_books_tidy.csv")
View(t_books)
View(t_books %>% filter(Author_Name == "Stephen King"))
names(t_books)
# guardo Year_published:
t_books %>% select(Year_published) %>% max()
t_books[which.min(t_books$Year_published),]
length(t_books[t_books$Year_published == 0,])
which(t_books$Year_published == 0)
# devo togliere questi libri dalle analisi che riguardano l'anno
length(which(t_books$Year_published < 1500))
classi_anni <- cut(t_books$Year_published, c(1900, 1970, 1980, 1990, 2000, 2010, 2022))
table(classi_anni)

View(t_books %>% filter(Year_published == 1818))

movies <- read_csv("movies_metadata.csv")
problems(movies)
spec(movies)
View(movies[19731,])
