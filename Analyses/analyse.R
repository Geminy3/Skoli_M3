library(tidyverse)
library(lubridate)
library(data.table)
library(patchwork)

getwd()

#### CHANGE THIS VALUE IF YOU ARE NOT IN THE GOOD FILE
path_to_file = "./Desktop/Projets/Skoli_M3/"

########### Imports

df <- fread(paste(path_to_file, "data_web.csv"))
DB <- fread(paste(path_to_file, "ezbinaryfile.csv"))

########### NETTOYAGE
DB_uni <- DB %>%
  group_by(contentobject_attribute_id) %>%
  slice(max(version))

df$IDinDB <- as.integer(df$IDinDB)

df <- df %>%
  filter(!is.na(IDinDB)) # On perd 719 docs

df <- df %>% distinct(TITRE, .keep_all = T) # On perd 389 docs

rbind(DB %>% nrow(), DB_uni %>% nrow(), df %>% nrow())

df$DATE <- df$DATE %>% lubridate::dmy() %>% as.Date()
df <- df %>%
  mutate(
    year = lubridate::year(DATE)
  )

DB_uni <- DB_uni %>%
  rename("IDinDB" = contentobject_attribute_id)

############ Jointure
jointdf <- df %>%
  inner_join(DB_uni, by = "IDinDB")

names(jointdf)
nrow(jointdf)  # On perd 173 docs

## Sur les 1809 docs que l'on a trouvé par scrapping, on a des URLS en double, 
## pas mal de page qui n'ont pas d'ID dans la base (719), et pas mal qui n'ont pas
## un ID que l'on retrouve dans la base.

## Il faudrait voir à récupérer plus de pages URLS (il en manque certainement)
## Du coup on a que 528 pages du site que l'on peut associer à un doc pdf. 
## GROS PB : Les PDFs sortent trop mal pour pouvoir vraiment être analysé. 

############ Analyses

### ARTICLE / AN

p1 <- df %>%
  ggplot(aes(x = year, group = year)) +
  geom_bar(aes(fill = year)) +
  labs(title = "Nb article par an", subtitle = "Tableau scrappé")


p2 <- jointdf %>%
  ggplot(aes(x = year, group = year)) +
  geom_bar(aes(fill = year)) +
  labs(title = "Nb article par an", subtitle = "Tableaux joints")

p1 + p2
############## TELECHARGEMENT
names(jointdf)

jointdf %>%
  ggplot(aes(x = year, y = download_count, group = year)) +
  geom_col(aes(fill = year))

