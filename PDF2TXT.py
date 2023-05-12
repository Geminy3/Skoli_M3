from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os
import PyPDF2
from PyPDF2 import PdfReader
import re


export_folder = "export2txt"
pdf_folder = "./dump/articles/"
error = []

def pdf2txt(path, output = False):

    doc = []
    for page_layout in extract_pages(path):
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        doc.append((element.get_text().replace('\n', " ").replace("\'", ' ')))
    if output:
        print(doc)

    return(doc)

def pdfminer():

    print("PDFMINER.SIX")
    for i, article in enumerate(os.listdir(pdf_folder)):
        print(f"\r{i}/{len(os.listdir(pdf_folder))} : {article}", end = "")

        if export_folder not in os.listdir("./"):
            os.mkdir(export_folder)
        try:
            doc = pdf2txt(pdf_folder+article)

            with open(export_folder+"/"+article.replace("pdf", "txt"), "w", encoding="utf-8") as writefile:
                writefile.writelines("".join(doc))
        except:
            print(f"{article} not in folder ?")
            for page_layout in extract_pages(pdf_folder+article):
                print("thre is a layout")
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        print("there is an instance")
                    else:
                        print("there is no instance")
            error.append(article)

def pypdf2txt(path, output = False):

    doc = []
    reader = PdfReader(path)
    for pages in reader.pages:
        doc.append(pages.extract_text().split("\n"))

    if output:
        print(doc)

    return(doc)

def pypdf():
    
    print("PyPDF2")
    for article in os.listdir(pdf_folder)[:1]:
        if export_folder not in os.listdir("./"):
            os.mkdir(export_folder)
        try:
            doc = pypdf2txt(pdf_folder+article)
        except:
            print(f"{article} not in folder ?")
    print(doc)

if __name__ == "__main__":
    #pdfminer()
    #pdf2txt(pdf_folder+"008b617a213cda74dacb384f11abf187.pdf",  output = True)
    #pypdf2txt(pdf_folder+"008b617a213cda74dacb384f11abf187.pdf",  output = True)
    print("change script to convert pdf to txt")
