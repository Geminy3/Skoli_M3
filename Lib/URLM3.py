import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
#from multiprocessing import Pool, Process
import os
import time

def get_all_page(urls, pattern, url_base):

    if pattern in urls:
        return(urls)
    
    html = requests.get(pattern)
    soup = BeautifulSoup(html.content, "html.parser")
    last_page = soup.find("a", {"title" : "Dernière page"})["page"]

    iter = soup.find_all("div", {"class" : re.compile("m3-pagination print_hidden|print_hidden pagination")})
    for item in iter:
        lst = re.findall("url.*?;", item.find_next_sibling().text)
        nw_url = ""
        if len(lst) > 0:
            for item in lst:
                if re.search("querystring", item):
                    continue
                else:
                    item = re.sub("url =|url \+=|url", "", item)
                    item = item.replace(";", "").replace("\"", "").strip()
                    item = item.split(" + ")
                for part in item:
                    nw_url += part
            match = re.compile("\$\(this\)\.attr\(page\)")
            for i in range(1, int(last_page)+1):
                url = urljoin(url_base, re.sub(match,str(i), nw_url))
                if url not in urls:
                    urls.append(url)
                    
        else:
            for i in range(1, int(last_page)+1):
                urls.append(urljoin(url_base, re.sub("page=.", f"page={i}", pattern)))
    
    return(urls)

def getAllUrl(url, url_base, urls, EXPORT_FILE, DATA_FOLDER, page):

    soup = BeautifulSoup(page.content, "html.parser")
    for anchor in soup.find_all("a"):
        if "href" in anchor.attrs:
            if anchor["href"] == "JavaScript:void(0);" and anchor["class"] == "lien-page":
                try:
                    urls.extend(get_all_page(urls), url, url_base)
                except:
                    continue
            absolute_url = urljoin(url_base, anchor["href"])
            if "download" not in absolute_url and absolute_url not in urls and anchor["href"] != "JavaScript:void(0);":
                if re.search(url_base, absolute_url):
                    urls.append(absolute_url)
    # Export des pages html ?
                    with open(DATA_FOLDER+EXPORT_FILE, "a", encoding="utf-8") as f:
                        f.write(absolute_url + '\n')

    return(urls)

def read_urls(EXPORT_FILE):
    with open(EXPORT_FILE, "r") as f:
        urls = f.read().split("\n") 
    print(len(urls))
    return(urls)

def getURLSM3(EXPORT_FILE, HTML_FOLDER, DATA_FOLDER, STATUS):
    
    verify = ""
    #STATUS = input( "What do you want to do ? [REBOOT][UPDATE][...] :\n")
    if STATUS == "REBOOT":
        verify = input("REBOOT entraînera la reconstitution complète de la base de données. Êtes-vous sûr de vouloir continuer ? [Y/n]:\n")
            
    
    url_base = 'https://www.millenaire3.com'
    errors = []
    clean_urls = []

    if STATUS == "REBOOT" and verify != "n":
        print("REBOOT")
        urls = get_all_page(urls = [], 
                    pattern="https://www.millenaire3.com/m3_search?page=1&sort_by=0&SearchText=&modeRecherche=1&titre=&auteurId=&auteurText=&100%25=&100%25_new_value=true&date_debut=01%2F01%2F1900&date_debut_mobile=&date_fin=31%2F12%2F2025&date_fin_mobile=&identifiers=&rubriques=",
                    url_base = url_base)
        with open(DATA_FOLDER+EXPORT_FILE, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url+'\n')
    
    # elif EXPORT_FILE in os.listdir(DATA_FOLDER) and STATUS != "UPDATE":
    #     print("LOAD")
    #     urls = read_urls(DATA_FOLDER+EXPORT_FILE)
        
    else:
        print("UPDATE")
        urls = get_all_page(urls = read_urls(DATA_FOLDER+EXPORT_FILE), 
                    pattern="https://www.millenaire3.com/m3_search?page=1&sort_by=0&SearchText=&modeRecherche=1&titre=&auteurId=&auteurText=&100%25=&100%25_new_value=true&date_debut=01%2F01%2F1900&date_debut_mobile=&date_fin=31%2F12%2F2025&date_fin_mobile=&identifiers=&rubriques=",
                    url_base = url_base)
        with open(DATA_FOLDER+EXPORT_FILE, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url+'\n')
        
    if verify != "n":
        files = os.listdir(HTML_FOLDER)
        i = 0 #len(files) ? # On peut changer la valeur de départ
        while i <= len(urls)-1:
            URL = urls[i].replace("/", "_").replace(".", "_").replace(":", "_").replace("?", "_").replace("=", "_").replace("&", "_").replace("%", "_").replace("-", "_").replace("httpswwwmillenaire3com", "_").replace("_", "")
            if f"{URL}.html" in files and STATUS != "REBOOT":
                pass
            elif re.search("/partage_email/|/generated_pdf/", urls[i]):
                #print(re.search("/partage_email/|/generated_pdf/", urls[i]))
                errors.append(urls[i])
                print(f"\r{i} / {len(urls)}, errors", end = "")
                pass
            else:
                print(f"\r{i} / {len(urls)}: {urls[i]}", end = "")
                try:
                    page = requests.get(urls[i])
                    if page.status_code == 200:
                        getAllUrl(urls[i], url_base, urls, EXPORT_FILE, DATA_FOLDER, page)
                        with open(f"{HTML_FOLDER}{URL}.html", "w", encoding="utf-8") as f:
                            clean_urls.append(urls[i])
                            f.write(page.text)
                    else:
                        print(f"\r{urls[i]} ", page.status_code, end = "")
                        errors.append(urls[i])
                    time.sleep(0.5)
                except:
                    print(f"Wrong URL : {urls[i]}")
            i += 1