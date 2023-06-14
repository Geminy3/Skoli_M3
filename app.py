from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pandas as pd


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.PULSE])

sidebar = html.Div([
                    html.H3("Millénaire3 Analysis"),
                    dbc.Nav(
                        [
                            dbc.NavLink(
                                [
                                    html.Div(page["name"], className="ms-2"),
                                ],
                                href=page["path"],
                                active="exact",
                            )
                            for page in dash.page_registry.values()
                        ],
                        vertical=True,
                        pills=True,
                        justified=True,
                        fill=True,
            )
])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, width = 2),
        dbc.Col(dash.page_container)
        ]),
    ], 
    fluid=True)

if __name__ == '__main__':
	app.run_server(debug=True)