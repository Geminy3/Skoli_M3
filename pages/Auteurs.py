from dash import Dash, html, dcc, callback
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import Lib.TEXT2DATA as text
IMPORT_FOLDER = "./data/"
df = pd.read_csv(IMPORT_FOLDER+"data_article_clean.csv")


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
aut_link = pd.read_csv("./pages/data/tag2aut.csv")
tag_db = pd.read_csv("./pages/data/tags_db.csv")
nOcc, tfidf = text.instanciate_method(IMPORT_FOLDER, df)


default = "Lucas PIESSAT"

main_div = html.Div(children=[
    html.Br(),
    html.H1(children="Analyse sur les auteurs"),

    html.Div(children=f'''
         Skoli - Alioscha Massein
    '''),
    html.Br(),
    html.Div([
        #html.H4("Auteurs tab"),
        #generate_table(aut),
        html.Div([
            dcc.Dropdown(aut['auteurs'].unique(), default, id='DropAut'),
            html.Br(),
            dcc.RangeSlider(
                min = aut[aut.auteurs == default]['YEAR'].min(),
                max = aut[aut.auteurs == default]['YEAR'].max(),
                id='year-sliderA',
                value=[aut[aut.auteurs == default]['YEAR'].min(), aut[aut.auteurs == default]['YEAR'].max()],
                marks={str(int(year)): str(int(year)) for year in aut[aut.auteurs == default]['YEAR'].unique()},
            ),
            html.Br(),
            dcc.Checklist(aut['TYPE'].unique(), aut['TYPE'].unique(), inline = True, id='DropTypeA'),

        ]),

        html.Br(),
        html.Div([
            dcc.Graph(id="Gaut1"),
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id="Gaut2")
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        html.Div([
            html.H3("Collaboration"),
            dcc.Graph(id="Gaut3")
        ]),
        html.Div([
            html.H3("Tags utilisés"),
            dcc.Graph(id="Gaut4")
        ]), 
        html.H3("Titre des contributions"),
        html.Div([
            dcc.Dropdown(tag_db['tags'].unique(), "Tous les articles", id='DropTagAut'),
        ], style = {'width': '49%', 'display': 'inline-block'}),
        # html.Div([
        #     dcc.Dropdown(net["target"].unique(), id='DropAutTag')
        # ], style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        html.Div([
            html.Br(),
            html.Ul(id = "title_p"),
            html.Br()
        ]),
        html.Br(),
        html.Div([
            html.H3("Observation des mots"),
            html.Br(),
            dcc.Slider(min = 1,
                       step = 1,
                       max = 100,
                       value = 10,
                       marks = None,
                       tooltip={"placement": "bottom", "always_visible": True},
                       id = "nb_rows"
                       )
        ]),
        html.Div([
            html.H3("Mots les plus fréquents pour\ncet auteur"),
            html.Div(id="table_aut", style={"width" : "50%", "margin": "auto"}),
            html.Br()
        ], style = {'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H3("Mots les plus spécifiques à cet auteur"),
            html.Div(id="table_aut_tfidf", style={"width" : "50%","margin": "auto"}),
        ], style = {'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ])
    
])

@callback(
    Output('Gaut1', 'figure'),
    Output("Gaut2", "figure"),
    Output("Gaut3", "figure"),
    Output("Gaut4", "figure"),
    Output("year-sliderA", "min"),
    Output("year-sliderA", "max"),
    Output("year-sliderA", "marks"),
    Output('DropTypeA', "options"),
    Input('DropAut', "value"),
    Input("year-sliderA", "value"),
    Input('DropTypeA', "value"),
)
def update_Gaut(auteur, year, type):

    min_y = int(year[0])
    max_y = int(year[1])
    #Gaut1
    filtered_df = pd.DataFrame({"values" : aut[aut.auteurs == auteur][aut.TYPE.isin(type)].YEAR.value_counts().sort_index(),
                                "year" : aut[aut.auteurs == auteur][aut.TYPE.isin(type)].YEAR.value_counts().sort_index().index})
    
    fig = px.bar(filtered_df, x = "year", y = "values")
    fig.update_layout(transition_duration = 500)
    
    #Gaut2
    filtered_df = pd.DataFrame({"values" : aut[aut.auteurs == auteur][aut.YEAR >= min_y][aut.YEAR <= max_y].TYPE.value_counts().sort_index(), 
                                "type" : aut[aut.auteurs == auteur][aut.YEAR >= min_y][aut.YEAR <= max_y].TYPE.value_counts().sort_index().index})
    
    fig2 = px.bar(filtered_df, x = "type", y = "values", color="type")
    fig2.update_layout(transition_duration = 500, showlegend=False)
    
    #Gaut3
    filtered_df = net[net.source == auteur].sort_values(by="values")
    fig3 = px.bar(filtered_df, x = "target", y = "values")
    fig3.update_layout(transition_duration = 500, showlegend=False, xaxis={'categoryorder':'total descending'})
    
    #Gaut4
    filtered_df = aut_link[aut_link.source == auteur].sort_values(by="values")
    fig4 = px.bar(filtered_df, x = "target", y = "values")
    fig4.update_layout(transition_duration = 500, showlegend=False, xaxis={'categoryorder':'total descending'})
    
    #Slider
    filtered_df = aut[aut.auteurs == auteur]
    min = filtered_df.YEAR.min()
    max = filtered_df.YEAR.max()
    marks = {}
    for year in aut[aut.auteurs == auteur]['YEAR'].unique():
        marks[str(int(year))] = str(int(year))
    #Dropdown_type
    options = aut[aut.auteurs == auteur].TYPE.unique()

    return(fig, fig2, fig3, fig4, min, max, marks, options)

@callback(
    Output("title_p", "children"),
    Output("DropTagAut", "options"),
    # Output('DropAutTag', "options"),
    Input("DropTagAut", "value"),
    Input('DropAut', "value"),
    # Input("DropAutTag", "value")
)
def title_aut(tag, auteur): #, sub_aut):

    urls = aut[aut.auteurs == auteur]["Unnamed: 0"]
    tmp = tag_db[tag_db.index.isin(urls)]
    options_tags = np.append(tmp.tags.unique(), "Tous les articles")
    # options_aut = np.append(net[net.source == auteur].target.unique(), "Tous les auteurs")

    if tag == "Tous les articles":
        urls = tmp.url.unique()
    else:
        tmp = tmp[tmp.tags == tag]
        urls = tmp.url.unique()
    # if sub_aut == 'Tous les auteurs':
    #     pass
    # else:

    #     pass
    data = pd.read_csv("./data/data_article_clean.csv")
    text = data[data.URL.isin(urls)].TITRE

    text = [html.Li(html.A(titre, href=data[data.TITRE == titre].URL.values[0], target="_blank")) for titre in text]

    return(text, options_tags) #, options_aut)

@callback(
        Output("table_aut", "children"),
        Output("table_aut_tfidf", "children"),
        Input('DropAut', "value"),
        Input('nb_rows', "value")
)
def table_aut_gen(auteur, nb_rows):

    text.get_an_aut_termdoc(tfidf, nOcc, auteur)
    path = f"./pages/data/Txt/Auteurs/Occurences/{auteur}.csv"
    dataframe = pd.read_csv(path)
    dataframe.columns = ["Termes", "Occurences"]

    nb_urls = len(aut[aut.auteurs == auteur])
    path_tfidf = f"./pages/data/Txt/Auteurs/TF_IDF/{auteur}.csv"
    dataframe_tfidf = pd.read_csv(path_tfidf)
    dataframe_tfidf.columns = ["Termes", "tf-idf"]
    dataframe_tfidf["tf-idf"] = round(dataframe_tfidf["tf-idf"] / nb_urls, 3)

    return(generate_table(dataframe, max_rows=nb_rows), generate_table(dataframe_tfidf, max_rows=nb_rows))

def layout():
    return(html.Div([
        main_div  # adjust width
            ])
    )
