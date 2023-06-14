from dash import Dash, html, dcc, callback
import dash
# import dash_core_components as dcc 
# import dash_html_components as html 
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

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

tag = pd.read_csv("./pages/data/tags_db.csv")
net = pd.read_csv("./pages/data/tags_link.csv")
# aut_link = pd.read_csv("./pages/data/tag2aut.csv") To DO

main_div = html.Div(children=[
    html.Br(),
    html.H1(children="Analyse sur les tags"),

    html.Div(children=f'''
         Skoli - Alioscha Massein
    '''),
    
    html.Br(),
    html.Div([
        #html.H4("Auteurs tab"),
        #generate_table(aut),
        dcc.Dropdown(tag['tags'].unique(), 'Mobilité', id='DropTag'),
        html.Br(),
        html.Div([
            dcc.Graph(id="Gtag1"),
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id="Gtag2")
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id="Gtag3")
        ], style={'width': '49%', 'display': 'inline-block'}),
        # html.Div([
        #     dcc.Graph(id="Gtag4")
        # ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ])
    
])

@callback(
    Output('Gtag1', 'figure'),
    Output("Gtag2", "figure"),
    Output("Gtag3", "figure"),
    # Output("Gtag4", "figure"),
    Input('DropTag', "value")
)
def update_Gaut(TAG):
    #Gaut1
    filtered_df = pd.DataFrame({"values" : tag[tag.tags == TAG].YEAR.value_counts().sort_index(),
                                "year" : tag[tag.tags == TAG].YEAR.value_counts().sort_index().index})
    
    fig = px.bar(filtered_df, x = "year", y = "values")
    fig.update_layout(transition_duration = 500)
    
    #Gaut2
    filtered_df = pd.DataFrame({"values" : tag[tag.tags == TAG].TYPE.value_counts().sort_index(), 
                                "type" : tag[tag.tags == TAG].TYPE.value_counts().sort_index().index})
    
    fig2 = px.bar(filtered_df, x = "type", y = "values", color="type")
    fig2.update_layout(transition_duration = 500, showlegend=False)
    
    #Gaut3
    filtered_df = net[net.source == TAG]
    fig3 = px.bar(filtered_df, x = "target", y = "values")
    fig3.update_layout(transition_duration = 500, showlegend=False)
    
    # #Gaut4
    # filtered_df = aut_link[aut_link.source == auteur]
    # fig4 = px.bar(filtered_df, x = "target", y = "values")
    # fig4.update_layout(transition_duration = 500, showlegend=False)
    
    return(fig, fig2, fig3)#, fig4)

def layout():
    return(html.Div([
        main_div  # adjust width
            ])
    )
