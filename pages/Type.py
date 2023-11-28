from dash import Dash, html, dcc, callback
import dash
# import dash_core_components as dcc 
# import dash_html_components as html 
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
#from side_bar import sidebar

dash.register_page(__name__)

def layout():
    return(
        html.Div([
            "In Progress"
        ])
    )