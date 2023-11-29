from dash import Dash, html, dcc, callback, State, ctx
import dash
from dash.dependencies import Input, Output
import Lib.update_pipeline as update
import Lib.URLM3 as url
import Lib.SCRAPM3 as scrap

dash.register_page(__name__)

main_div = html.Div([
    html.Br(),
    html.H1("UPDATE DataBase"),
    html.Br(),
    html.P("""
Cette page permet de mettre à jour les données du site.\n
Faites attention, cette procédure peut prendre un peu de temps. 
"""),
    html.Button("Mettre à jour", id="Update_button"),
    html.Br(),
    html.Div(id="Update_output", children=""),
    html.Div(id="final_output", children = "")
])

@callback(
        Output("final_output", "children"),
        Input("Update_button", "n_clicks"),
        running = [
            (Output("Update_button", "disabled"), True, False)
        ],
        progress=[Output("Update_output", "children")],
        prevent_initial_call=True,
        background=True,
)
def updates(set_progress, n_clicks):
    if "Update_button" == ctx.triggered_id:
        set_progress(["Mise à jour en cours. Téléchargement html de M3"])
        url.getURLSM3(EXPORT_FILE="M3urls3.txt", 
               HTML_FOLDER="./urls/", 
               DATA_FOLDER="./data/",
               STATUS="UPDATE")
        set_progress(["Corpus télécharge. Scrapping en cours"])
        scrap.scrapM3(EXPORT_FOLDER = "./data/", 
               HTML_FOLDER = "./urls/", 
               DATA_FOLDER = "./data/", 
               EXPORT_FILE = "M3urls3.txt")
        set_progress(["Corpus mis à jour, construction des données"])
        update.update_net_data()
        set_progress(["Data mises à jour, extraction des éléments de texte"])
        update.update_nlp_elem()

        return("Mise à jour terminée")

def layout():
    return(main_div)
