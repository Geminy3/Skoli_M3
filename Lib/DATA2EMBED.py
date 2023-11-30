from langchain.document_loaders import TextLoader
from langchain.embeddings import LlamaCppEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import LlamaCpp
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import HuggingFaceEmbeddings
import json
import pickle
import re
import os
import tarfile
import shutil


with open("api_key", "r", encoding="utf-8") as key:
    api_key = key.read()

with open("HF_api_key", "r", encoding="utf-8") as key:
    HF_api_key = key.read()

### WATCH OUT !
orga_key = "org-mqd2akvmI5TNokavyM3mW"

embeddings_model_name="all-MiniLM-L6-v2"

# Sentence_transformers
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, model_kwargs={'device' : 'cpu'})

# # Llama2 (Couldn't create embeddings for now (more than a day of computing))
# n_gpu_layers = 35  # Change this value based on your model and your GPU VRAM pool.
# n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
# #llama = LlamaCppEmbeddings(model_path="./llama-2-7b-chat.ggmlv3.q4_0.bin", n_ctx = 4096, f16_kv=True, n_gpu_layers=n_gpu_layers, n_batch=n_batch)

def make_chroma_db():

    loaders = []
    docs = []

    path = "./data/Texte/"
    listdir = os.listdir(path)
    listdir.sort(key=lambda x:int(x))

    for i, folder in enumerate(listdir):
        print(f"\r{i} / {len(listdir)}", end = "")
        f_path = os.path.join(path, folder)
        for file in os.listdir(f_path):
            if file == "full.txt":
                file_path = os.path.join(f_path, file)
                loaders.append(TextLoader(file_path, encoding="utf-8"))
                
    for i, loader in enumerate(loaders):
        print(f"\r{i} / {len(loaders)}", end = "")
        docs.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4096, chunk_overlap=300, length_function = len, add_start_index = True)
    documents = text_splitter.split_documents(docs)

    print(f"\nNombre de documents : {len(documents)}")

    Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory="./Lib/chroma")