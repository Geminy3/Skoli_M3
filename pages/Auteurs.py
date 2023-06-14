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


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

aut = pd.read_csv("./pages/data/auteurs_db.csv")
net = pd.read_csv("./pages/data/auteurs_link.csv")
aut_link = pd.read_csv("./pages/data/aut2tag.csv")

main_div = html.Div(children=[
    html.Br(),
    html.H1(children="Analyse sur les auteurs"),

    html.Div(children=f'''
         A web application framework for your data.
    '''),
    
    html.Div([
        #html.H4("Auteurs tab"),
        #generate_table(aut),
        dcc.Dropdown(aut['auteurs'].unique(), 'Lucas PIESSAT', id='DropAut'),
        html.Div([
            dcc.Graph(id="Gaut1"),
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id="Gaut2")
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id="Gaut3")
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id="Gaut4")
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ])
    
])

@callback(
    Output('Gaut1', 'figure'),
    Output("Gaut2", "figure"),
    Output("Gaut3", "figure"),
    Output("Gaut4", "figure"),
    Input('DropAut', "value")
)
def update_Gaut(auteur):
    #Gaut1
    filtered_df = pd.DataFrame({"values" : aut[aut.auteurs == auteur].YEAR.value_counts().sort_index(),
                                "year" : aut[aut.auteurs == auteur].YEAR.value_counts().sort_index().index})
    
    fig = px.bar(filtered_df, x = "year", y = "values")
    fig.update_layout(transition_duration = 500)
    
    #Gaut2
    filtered_df = pd.DataFrame({"values" : aut[aut.auteurs == auteur].TYPE.value_counts().sort_index(), 
                                "type" : aut[aut.auteurs == auteur].TYPE.value_counts().sort_index().index})
    
    fig2 = px.bar(filtered_df, x = "type", y = "values", color="type")
    fig2.update_layout(transition_duration = 500, showlegend=False)
    
    #Gaut3
    filtered_df = net[net.source == auteur]
    fig3 = px.bar(filtered_df, x = "target", y = "values")
    fig3.update_layout(transition_duration = 500, showlegend=False)
    
    #Gaut4
    filtered_df = aut_link[aut_link.source == auteur]
    fig4 = px.bar(filtered_df, x = "target", y = "values")
    fig4.update_layout(transition_duration = 500, showlegend=False)
    
    return(fig, fig2, fig3, fig4)

def layout():
    return(html.Div([
        main_div  # adjust width
            ])
    )
