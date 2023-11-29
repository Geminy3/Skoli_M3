from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager
import dash
import plotly.express as px
import pandas as pd
import diskcache

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = Dash(__name__, 
		   use_pages=True,
		   long_callback_manager=long_callback_manager,
		   external_stylesheets=[dbc.themes.PULSE]
		   )


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
        dbc.Col(sidebar, width = 2,
		        class_name='border',
                xs = 12, md  = 2),
        dbc.Col(dash.page_container,
		        style={'min-height':'100vh'},
                class_name='border',
                xs = 12 , md  = 10)
        ]),
    ], 
    fluid=True)

if __name__ == '__main__':
	app.run_server(debug=True)