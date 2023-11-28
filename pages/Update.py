from dash import Dash, html, dcc, callback, State, ctx
import dash
from dash.dependencies import Input, Output
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import Lib.update_pipeline as update
import re

dash.register_page(__name__)

main_div = html.Div([
    html.Br(),
    html.H1("UPDATE - DB"),
    html.Br(),
    html.P("""
Cette page permet de mettre à jour les données du site.\n
Faites attention, cette procédure peut prendre un peu de temps. 
"""),
    html.Button("Mettre à jour", id="Update_button"),
    html.Br(),
    html.Div(id="Update_output", children="")
])

@callback(
        Output("Update_output", "children"),
        Input("Update_button", "n_clicks"),
        prevent_initial_call=True
)
def updates(n_clicks):
    if "Update_button" == ctx.triggered_id:
        return("Implémentation en cours "+str(n_clicks))

def layout():
    return(main_div)
