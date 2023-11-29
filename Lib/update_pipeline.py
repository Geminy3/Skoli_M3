import Lib.URLM3 as url
import Lib.SCRAPM3 as scrap
import Lib.DATA2NET as net
import Lib.TEXT2DATA as text
import Lib.DATA2EMBED as embed
import pandas as pd
import spacy

def update_corpus():

    url.getURLSM3(EXPORT_FILE="M3urls3.txt", 
                HTML_FOLDER="./urls/", 
                DATA_FOLDER="./data/",
                STATUS="UPDATE")


    scrap.scrapM3(EXPORT_FOLDER = "./data/", 
                HTML_FOLDER = "./urls/", 
                DATA_FOLDER = "./data/", 
                EXPORT_FILE = "M3urls3.txt")



def update_net_data():

    mult_items = net.get_mult_item()
    EXPORT_FOLDER = "./res/"
    net.tag_net(EXPORT_FOLDER, mult_items)
    print('UPDATING NET')

    net.auteurs_net(EXPORT_FOLDER, mult_items)
    print('UPDATING NET')

    net.tag2aut(EXPORT_FOLDER, mult_items)
    print('UPDATING NET')

    net.auteurs_net2(EXPORT_FOLDER, mult_items)
    print('UPDATING NET')

    net.tag_net2(EXPORT_FOLDER, mult_items)
    print('UPDATING NET')

    net.auteurs_links(mult_items)
    print('UPDATING NET')

    net.tag_links(mult_items)
    print('UPDATING NET')

    IMPORT_FOLDER = "./data/"
    df = pd.read_csv(IMPORT_FOLDER+"data_article_clean.csv")
    net.auteurs_db(df)
    net.tags_db(df)
    print('UPDATING NET')

def update_nlp_elem():
    IMPORT_FOLDER = "./data/"
    df = pd.read_csv(IMPORT_FOLDER+"data_article_clean.csv")

    #nlp_max = fr_dep_news_trf.load()
    nlp_eff = spacy.load("fr_core_news_sm")
    text.get_lemma(nlp = nlp_eff, df = df, EXPORT_FOLDER = IMPORT_FOLDER)

    # Generate Embeddings
    embed.make_chroma_db()