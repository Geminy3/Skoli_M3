from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os
import PyPDF2
from PyPDF2 import PdfReader
import re


export_folder = "export2txt"
pdf_folder = "./dump/articles/"
error = []

print("PDFMINER.SIX")
for i, article in enumerate(os.listdir(pdf_folder)):
    print(f"\r{i}/{len(os.listdir(pdf_folder))} : {article}", end = "")
    doc = []
    if export_folder not in os.listdir("./"):
        os.mkdir(export_folder)
    try:
        for page_layout in extract_pages(pdf_folder+article):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    doc.append((element.get_text().replace('\n', " ").replace("\'", ' ')))

        # print("".join(doc))
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
    

# print("PyPDF2")
# for article in os.listdir(pdf_folder)[:1]:
#     doc = []
#     if export_folder not in os.listdir("./"):
#         os.mkdir(export_folder)
#     try:
#         reader = PdfReader(pdf_folder+article)
#         print(article)
#         for pages in reader.pages:
#             doc.append(pages.extract_text().split("\n"))
#     except:
#         print(f"{article} not in folder ?")
# print(doc)