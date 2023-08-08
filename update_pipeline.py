from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
#from multiprocessing import Pool, Process
import os
import time
import pandas as pd
import requests
import json
import pandas as pd
import Lib.URLM3
import Lib.SCRAPM3

EXPORT_FILE = "M3urls3.txt"
HTML_FOLDER = "../urls/"
DATA_FOLDER = "../data/"

Lib.URLM3.getURLSM3(EXPORT_FILE, HTML_FOLDER, DATA_FOLDER)

EXPORT_FOLDER = "../data2/"

Lib.SCRAPM3.scrapM3(EXPORT_FOLDER, HTML_FOLDER, DATA_FOLDER, EXPORT_FILE)


#### TO DO
#
# 1. Les fichiers du dossier ./res issus des manip de Analyse_reseau
# 2. Récupérer les manips pour la création des fichiers textes Analyse_items + Analyse_text
# 3. Produire toutes les ressources textes pour le site. 
# 4. Annoter le code
# 5. Prévoir que le déploiement soit simple (Makefile ?)
# 6. OU intégrer des outils dans le site pour MAJ.


#### BUGS
#
# 1. Problème dans le chargement des articles sur le site M3. Moins d'article à la seconde passe
# 2. Pas résolu le problème de connection aborted dans la récupération des URLs (Try/Except enlevé)
