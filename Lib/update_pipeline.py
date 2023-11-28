import Lib.URLM3 as url
import Lib.SCRAPM3 as scrap
import Lib.DATA2NET as net
import Lib.TEXT2DATA as text
import Lib.DATA2EMBED as embed
import pandas as pd
import spacy

def update_pipe():

    url.getURLSM3(EXPORT_FILE="M3urls3.txt", 
                HTML_FOLDER="./urls/", 
                DATA_FOLDER="./data/",
                STATUS="UPDATE")


    scrap.scrapM3(EXPORT_FOLDER = "./data/", 
                HTML_FOLDER = "./urls/", 
                DATA_FOLDER = "./data/", 
                EXPORT_FILE = "M3urls3.txt")


    #Création de la data
    ## RESEAU

    mult_items = net.mult_items

    EXPORT_FOLDER = "./res/"
    net.tag_net(EXPORT_FOLDER, mult_items)
    net.auteurs_net(EXPORT_FOLDER, mult_items)
    net.tag2aut(EXPORT_FOLDER, mult_items)
    net.auteurs_net2(EXPORT_FOLDER, mult_items)
    net.tag_net2(EXPORT_FOLDER, mult_items)
    net.auteurs_links(mult_items)
    net.tag_links(mult_items)

    IMPORT_FOLDER = "./data/"
    df = pd.read_csv(IMPORT_FOLDER+"data_article_clean.csv")
    net.auteurs_db(df)
    net.tags_db(df)

    #nlp_max = fr_dep_news_trf.load()
    nlp_eff = spacy.load("fr_core_news_sm")
    text.get_lemma(nlp = nlp_eff, df = df, EXPORT_FOLDER = IMPORT_FOLDER)

    nOcc, tfidf = text.instanciate_method(IMPORT_FOLDER, df)
    text.get_aut_term_doc(tfidf, nOcc)
    text.get_tags_term_doc(tfidf, nOcc)

    # Generate Embeddings
    embed.make_chroma_db()