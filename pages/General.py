from dash import Dash, html, dcc, callback
import dash
# import dash_core_components as dcc 
# import dash_html_components as html 
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path="/")

main_div = html.Div([
    html.Br(),
    html.H2("Ceci est un site d'analyse pour les données récoltées du site Millénaire 3"),
    html.P("Cette page est en cours de réalisation")
])

def layout():
    
    return(main_div)