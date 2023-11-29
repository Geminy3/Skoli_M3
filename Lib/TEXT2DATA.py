import spacy
#import spacy_transformers
import pathlib
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import pandas as pd

def get_lemma(nlp, df, EXPORT_FOLDER):

    rows, cols = df.shape 

    for row in range(rows):
        txt = []
        art = str(df.iloc[row].ARTICLE)
        res = str(df.iloc[row].RESUME)
        titre = str(df.iloc[row].TITRE)
        id = df.iloc[row]["Unnamed: 0"]
        
        full = titre+'\n'+res+'\n'+art
        doc2 = nlp(res+'\n'+art)
        
        for token in doc2:
            if token.is_stop == False :#and token.pos_ != "PUNCT":
                txt.append(token.lemma_)
            
        pathlib.Path(f'{EXPORT_FOLDER}Texte/{id}').mkdir(parents=True, exist_ok=True)
        with open(f"{EXPORT_FOLDER}Texte/{id}/full.txt", "w", encoding="utf8") as f:
            f.write(full)
        with open(f"{EXPORT_FOLDER}Texte/{id}/texte.txt", "w", encoding="utf8") as f:
            f.write(" ".join(txt))
        
        print(f"\rSuccessfuly exported {row} / {rows} : {txt[0:10]}", end="")
    


def instanciate_method(IMPORT_FOLDER, df):

    fichiers = glob.glob(IMPORT_FOLDER+"Texte/*/texte.txt")
    nOcc = {}
    documents=[]
    urls=[]
    for fichier in fichiers:
        idx = fichier.split("/")[3]
        url = df[df["Unnamed: 0"] == int(idx)].URL.values[0]
        urls.append(url)
        with open(fichier, encoding='utf8') as f:
            documents.append(f.read())
    counter=CountVectorizer()
    nOcc=counter.fit_transform(documents)
    nOcc=pd.DataFrame.sparse.from_spmatrix(nOcc,index=urls,columns=counter.get_feature_names_out())

    tfidfer=TfidfVectorizer(lowercase=False) #On ne maîtrise pas bien la tokennisation de CountVectorizer !
    tfidf_sklearn=tfidfer.fit_transform(documents)
    tfidf_sklearn=pd.DataFrame.sparse.from_spmatrix(tfidf_sklearn,index=urls,columns=tfidfer.get_feature_names_out())

    return(nOcc, tfidf_sklearn)


#### To export tag term_doc matrices
def get_tags_term_doc(tfidf_sklearn, nOcc):

    methods = ["tfidf", "Occ"]

    for method in methods:
        print(method)
        if method == "tfidf":
            method = tfidf_sklearn
            export = "TF_IDF"
        else:
            method = nOcc
            export = "Occurences"

        tag_info = pd.read_csv("./pages/data/tags_db.csv", index_col=0)

        for i, tag in enumerate(tag_info.tags.unique()):
            tmp = tag_info[tag_info.tags == tag].index
            print(tag, i, "/", len(tag_info.tags.unique()), "Nb_urls :", len(tmp))
            tmp2 = method[method.index.isin(tmp)].sum()
            tmp2 = tmp2[tmp2 > 0].sort_values(ascending=False)
            tmp2.to_csv(f"./pages/data/Txt/Tags/{export}/{tag}.csv")

def get_a_tag_termdoc(tfidf_sklearn, nOcc, tag):

    methods = ["tfidf", "Occ"]

    for method in methods:
        print(method)
        if method == "tfidf":
            method = tfidf_sklearn
            export = "TF_IDF"
        else:
            method = nOcc
            export = "Occurences"

        tag_info = pd.read_csv("./pages/data/tags_db.csv", index_col=0)
        tmp = tag_info[tag_info.tags == tag].index
        tmp2 = method[method.index.isin(tmp)].sum()
        tmp2 = tmp2[tmp2 > 0].sort_values(ascending=False)
        tmp2.to_csv(f"./pages/data/Txt/Tags/{export}/{tag}.csv")

def get_aut_term_doc(tfidf_sklearn, nOcc):

    methods = ["tfidf", "Occ"]

    for method in methods:
        print(method)
        if method == "tfidf":
            method = tfidf_sklearn
            export = "TF_IDF"
        else:
            method = nOcc
            export = "Occurences"

        aut_info = pd.read_csv("./pages/data/auteurs_db.csv", index_col=0)

        for i, auteur in enumerate(aut_info.auteurs.unique()):
            tmp = aut_info[aut_info.auteurs == auteur].index
            print(auteur, i, "/", len(aut_info.auteurs.unique()), "Nb_urls :", len(tmp))
            tmp2 = method[method.index.isin(tmp)].sum()
            tmp2 = tmp2[tmp2 > 0].sort_values(ascending=False)
            tmp2.to_csv(f"./pages/data/Txt/Auteurs/{export}/{auteur}.csv")

def get_an_aut_termdoc(tfidf_sklearn, nOcc, auteur):

    methods = ["tfidf", "Occ"]

    for method in methods:
        print(method)
        if method == "tfidf":
            method = tfidf_sklearn
            export = "TF_IDF"
        else:
            method = nOcc
            export = "Occurences"

        aut_info = pd.read_csv("./pages/data/auteurs_db.csv", index_col=0)

        tmp = aut_info[aut_info.auteurs == auteur].index
        tmp2 = method[method.index.isin(tmp)].sum()
        tmp2 = tmp2[tmp2 > 0].sort_values(ascending=False)
        tmp2.to_csv(f"./pages/data/Txt/Auteurs/{export}/{auteur}.csv")