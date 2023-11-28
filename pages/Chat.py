from dash import Dash, html, dcc, callback, State
import dash
from dash.dependencies import Input, Output
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from Lib.chat import chat
import re

dash.register_page(__name__)

def out_prompt(out):
    i = 0
    j = 0
    texte = ""
    while j < len(out):
        charac = out[j]
        if charac == ".":
            if re.search("etc", out[j-5:j]):
                texte += charac
                pass
            else:
                i = 0
                texte += charac + "\n\n"
                j += 1
        elif i >= 100:
            if charac != " ":
                texte += charac
            else:
                texte += "\n"
                i = 0
        else:
            texte += charac
        i += 1
        j += 1
        
    return(texte)

#### Ecrire le code pour charger la base de donénes et l'interroger
### -> Avec des fonctions

# embeddings_model_name="all-MiniLM-L6-v2"
# embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, model_kwargs={'device' : 'cpu'})

# vectorstore2 = Chroma(persist_directory = "./TEST_chat/chroma", embedding_function=embeddings)
# n_gpu_layers = 20
# n_batch = 512
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

main_div = html.Div([
    html.Br(),
    html.H2("Chat personnalisé"),
    html.Br(),
    html.Div([
        dcc.Textarea(value = "", placeholder = "Posez une question", id="inChat", style = {"width" : "80%"}),
        html.Br(),
        html.Button("Envoyer", id = "submit_button", n_clicks=0),
    ]),
    html.Br(),
    html.P(id = "outChat", style = {'whitespace': 'pre-line'}),
    html.Br(),
    html.H3("---------- DOCUMENTS -----------"),
    html.Div(id = "outDocs", style = {'whitespace': 'pre-line'})
    
])

@callback(
    Output("outChat", "children"),
    Output("outDocs", "children"),
    Input("submit_button", "n_clicks"),
    State("inChat", "value"),
)
def interrogate_chat(n_clicks, value):
    if value == "":
        return("En attente d'une question", html.Ul([html.Li("En attente de documents")]))
    out = chat(llm_info = "OAI", kMos = 50, question = value)
    ret = out["result"]
    docs = html.Ul([html.Li(str(x)) for x in out["source_documents"]])
    return(ret, docs)

def layout():
    return(main_div)
