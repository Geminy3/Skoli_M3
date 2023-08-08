from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import os

def get_metadata(soup, type, url, mult_items, errors):

    mult_items[url] = {"auteurs" : [], "tags" : [], "liens" : []}

    #TAGS
    tags_liste = soup.find_all("ul", {"class": "list-inline keywords"})
    tags = []
    for tag in tags_liste:
        a = tag.find_all("a")
        for tag in a:
            if re.search("tag", tag["href"]) != None:
                tags += tag.contents
    if len(tags) > 0:
        mult_items[url]["tags"] = tags
    else:
        mult_items[url]["tags"] = "NA"

    #AUTHORS
    if type == "Interview":
        liste = soup.find_all("ul", {"class": "list-inline keywords"})
        authors = []
        for elem in liste:
            a = elem.find_all("a")
            for author in a:
                if re.search("auteurs", author["href"]) != None:
                    authors.append(author.contents[0].strip())
    else:
        auth = soup.find_all("span", {"class" : "author-name"})
        authors = []
        for author in auth:
            author = repr(author.text).replace("\\xa0", " ").replace("\\t", "").replace("\\n", "").replace("'", "")
            if author not in authors:
                authors.append(author)
    if len(authors) > 0:
        mult_items[url]["auteurs"] = authors
    else:
        mult_items[url]["auteurs"] = "NA"
        
    #Liens
    page_links = soup.find_all("h3", {"class" : "h3 uppercase"})
    links = []
    for link in page_links:
        links.append("https://www.millenaire3.com"+link.a["href"])
    if len(links) > 0:
        mult_items[url]["liens"] = links
    else:
        mult_items[url]["liens"] = "NA"
    
    return(mult_items, errors)

def get_article_info(soup, type, url, container, errors):

    #RESUME
    if type == "Dossier":
        resume = soup.find("div", {"class" : "eztext-field"})
    elif type == "Interview":
        resume = soup.find("div", {"class" : "ezrichtext-field"})
    else: 
        resume = soup.find("div", {"class" : "eztext-field"})
    if len(resume) > 0:
        container["RESUME"].append(resume.text)
    else:
        errors["RESUME"].append(url)
        container["RESUME"].append("NA")

    #ARTICLE
    if type != "Interview":
        try:
            article = soup.find("div",  {"class" : "ezrichtext-field"}).text
        except:
            article = ""
    else:
        lines = soup.find_all("div", {"class" : "interview-item"})
        if len(lines) == 0:
            art = soup.find_all("div",  {"class" : "ezrichtext-field"})
            for info in art:
                if info != resume.text:
                    article = info.text
        else:
            article = ""
            for i, line in enumerate(lines):
                article += line.find("p", {"class" : "over-under-line"}).text + " "
                temp = line.find_all("div", {"class" : "ezrichtext-field"})
                for info in temp:
                    article += info.find("p").text
    if len(article) > 0:
        container["ARTICLE"].append(article.replace("\n", " "))
    else:
        errors["ARTICLE"].append(url)
        container["ARTICLE"].append("NA")

    #TITRE
    titre = soup.find("h1", {"class": "uppercase h1-special"}).contents[0]
    titre = titre.replace("\n", "").replace("\t", "").strip()
    if len(titre) > 0:
        container["TITRE"].append(titre)
    else:
        errors["TITRE"].append(url)
        container["TITRE"].append("NA")
        
    #ID - in db
    try:
        ID = soup.find("article", {"class" : "sidebar-block-classic sidebar-block-download"})
        ID = ID.a["href"].split("/")
        ID = ID[len(ID)-1]
        container["IDinDB"].append(ID)
    except:
        container["IDinDB"].append("NA")

    #DATE
    date = soup.find("span", {"class" : "publication_date"}).text
    if len(date) > 0:
        container["DATE"].append(date)
    else:
        errors["DATE"].append(url)
        container["DATE"].append("NA")
    
    #URL
    container["URL"].append(url)
    return(container, errors)

def scrap_page(page, container, mult_items, errors, HTML_FOLDER, url, ONLY_MULT = False):
    
    # html = requests.get(url)
    # if(html.status_code) != 200:
    #     print(html.status_code)
    #     errors["deadlink"].append(url)
    #     return(1)
    # soup = BeautifulSoup(html.text, "html.parser")
    with open(HTML_FOLDER+page, "r", encoding="utf8") as f:
        html= f.read()
    soup = BeautifulSoup(html, "html.parser")
    
    #TYPE
    type_liste = soup.find_all("p", {"class" : re.compile("^over-under")})
    if len(type_liste) > 0:
        type = ""
        for typ in type_liste:
            if re.search("Étude|Dossier|Article|Texte|Interview", typ.text) == None:
                continue
            else:
                if re.search("Interview|Texte", typ.text) == None:
                    type = typ.text.replace("\n", "").replace("\t", "").replace(" ", "")
                elif re.search("Texte", typ.text) != None:
                    type = "Texte"
                    txt_de = typ.text.replace("\n", "").replace("\t", "")
                elif re.search("Interview", typ.text) != None:
                    type = "Interview"
                    itw_de = typ.text.replace("\n", "").replace("\t", "")
    else:
        return(1)
    if len(type) > 0:
        container["TYPE"].append(type)
    else:
        errors["TYPE"].append(url)
        return(1)
    #END TYPE

    if ONLY_MULT == True:
        get_metadata(soup, type, url, mult_items, errors)
    else:
        get_article_info(soup, type, url, container, errors)
        get_metadata(soup, type, url, mult_items, errors)

    return(container, mult_items, errors)

def scrapM3(EXPORT_FOLDER, HTML_FOLDER, DATA_FOLDER, EXPORT_FILE): 
    ONLY_MULT = False

    with open(DATA_FOLDER+EXPORT_FILE, "r") as f:
            uris = f.read().split("\n")

    uris2 = [uri.replace("/", "_").replace(".", "_").replace(":", "_").replace("?", "_").replace("=", "_").replace("&", "_").replace("%", "_").replace("-", "_").replace("httpswwwmillenaire3com", "_").replace("_", "") for uri in uris]

    urls = os.listdir(HTML_FOLDER)
    #urls.sort(key = lambda x: int(x.replace(".html", "")))

    container = {"URL" : [], 
                    "TITRE" : [], 
                    "IDinDB" : [], 
                    "TYPE" : [], 
                    "RESUME" : [], 
                    "ARTICLE" : [],
                    "DATE" : []}

    mult_items = {}

    errors = {
            "TITRE" : [],
            "TYPE" : [],
            "RESUME" : [],
            "ARTICLE" : [],
            "DATE" : [],
            "deadlink" : []
        }

    for i, url in enumerate(urls):
        uri = uris[uris2.index(url.replace(".html", ""))]
        print(f"""\r{i}/{len(urls)} : {url}, {url.replace(".html", "")} : {uri}""", end = "")
        if re.search("/ressources/|/Interviews/|/dossiers/|/actualites-a-la-une/|/publications/", uri) and len(url) > 0:
            scrap_page(url, container, mult_items, errors, HTML_FOLDER, uri, ONLY_MULT)
        else:
            pass
            #print("not an article")


    for keys in container:
        print(keys, ":", len(container[keys]))
        
        
    ### EXPORT MULT_ITEM
    with open(EXPORT_FOLDER+"data_items.json", "w", encoding="utf8") as f:
        f.write(json.dumps(mult_items, indent=4))
        
    ### EXPORT ARTICLE_DATA
    tab = pd.DataFrame(container)
    tab.to_csv(EXPORT_FOLDER+"data_article.csv")
    # tab.DATE = pd.to_datetime(tab.DATE) #On mac
    # tab.DATE = pd.to_datetime(tab.DATE, format="%d/%m/%y") #On mac
    
    
    ### CLEANING ARTICLE_DATA
    tab.DATE = pd.to_datetime(tab.DATE, format="mixed", dayfirst=True) #On PC
    df2 = tab.loc[tab.TITRE.duplicated() != True,].sort_values(by="IDinDB")
    dfnotna = df2.loc[df2.IDinDB.notna()]
    print(f"No NA : {dfnotna.shape}\nWith NA : {df2.shape}")
    df2["YEAR"] = df2.DATE.dt.year
    df2.to_csv(EXPORT_FOLDER+"data_article_clean.csv")
    
    ### CLEANING MULT_ITEMS DATA
    print("length mult_items base", len(mult_items.keys()))
    dedoubl = pd.read_csv(EXPORT_FOLDER+"data_article_clean.csv")
    remove_list = list(set(mult_items.keys()) - set(list(dedoubl.URL)))
    for item in remove_list:    
        del mult_items[item]
    with open(EXPORT_FOLDER+"data_items_clean.json", "w", encoding="utf8") as f:
        f.write(json.dumps(mult_items, indent=4))
    print("length mult-items dédoublonné", len(mult_items.keys()))
    print("lenght df dédoublonné", len(dedoubl))
    
    