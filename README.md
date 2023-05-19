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
* Premières analyses : Surtout pour observer le nombre d'articles récupérer et produire quelques infos pour voir si notre corpus est exploitable
* Analyse_text : en cours de construction

## Objectifs

* Construire un outil de fouille :
    * Produire des résumés des articles/résumés (pré-traiter avec ChatGPT ?) pour voir comment un sujet est traité (en fonction de mots-clés) = Utiliser gensim/équivalent pour produire un index basé sur la similarité cosinus = Pas tant de docs que ça au final donc ça devrait le faire + Gensim a une fonction de stream qui ne charge pas trop la mémoire (à voir comment on update ça)
    * Produire de l'intelligence pour la métropole : dataviz et information macro (utiliser les tags, les auteurs,...) + Thématiques ? On part surtout des tags pour pas avoir à gérer une usine à gaz. 