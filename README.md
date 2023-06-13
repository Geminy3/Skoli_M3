# Skoli_M3

Ensemble de programme pour :

* Transformer les ressource PDF de M3 en TXT (pas concluant, beaucoup de texte qui ressortent mal, dans tous les cas difficile d'avoir des tokens propres)
* Récuperer (au mieux) l'ensemble des URLS du site M3
* Scrapper les urls, classer les données en plusieurs variables :
    * Type d'article
    * URL (ID)
    * TITRE
    * RESUME
    * ARTICLE
    * ID in database (ifany)
    * DATE
    * Auteurs
    * Tags
    * Liens
* Analyse_items : Surtout pour observer le nombre d'articles récupérer et produire quelques infos pour voir si notre corpus est exploitable. On analyse également les productions :
    * par auteurs
    * par tags
    * dans le temps...
* Analyse_reseau : Pour produire les fichiers json que l'on donne à cytoscape
    * Bug lié aux doublons des articles : peut-être faie une jointure en premier lieu sur un .csv dédoublonné ?
* Analyse_text : en cours de construction

## Objectifs

* Construire un outil de fouille :
    * Produire des résumés des articles/résumés (pré-traiter avec ChatGPT ?) pour voir comment un sujet est traité (en fonction de mots-clés) = Utiliser gensim/équivalent pour produire un index basé sur la similarité cosinus = Pas tant de docs que ça au final donc ça devrait le faire + Gensim a une fonction de stream qui ne charge pas trop la mémoire (à voir comment on update ça)
    * Produire de l'intelligence pour la métropole : dataviz et information macro (utiliser les tags, les auteurs,...) + Thématiques ? On part surtout des tags pour pas avoir à gérer une usine à gaz. Mais analyse du texte est nécessaire. Notamment pour savoir les occurences des mots de l'ensemble, par type, par année, par auteurs...

## BUGS TO FIX :

* Problème avec le scraping : connection abort sur la 7888e urls (on peut relancer pour remplir le dictionnaire à partir de là) -- Resolu
* Doublons dans les réseaux