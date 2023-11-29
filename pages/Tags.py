from dash import Dash, html, dcc, callback
import dash
# import dash_core_components as dcc 
# import dash_html_components as html 
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

tag = pd.read_csv("./pages/data/tags_db.csv")
net = pd.read_csv("./pages/data/tags_link.csv")
tag_link = pd.read_csv("./pages/data/tag2aut.csv")
aut_db = pd.read_csv("./pages/data/auteurs_db.csv")
nOcc, tfidf = text.instanciate_method(IMPORT_FOLDER, df)

default = 'Mobilité'


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
        html.Div([
            dcc.Dropdown(tag['tags'].unique(), default, id='DropTag'),
            html.Br(),
            dcc.RangeSlider(
                min = tag[tag.tags == default]['YEAR'].min(),
                max = tag[tag.tags == default]['YEAR'].max(),
                id='year-sliderT',
                value=[tag[tag.tags == default]['YEAR'].min(), tag[tag.tags == default]['YEAR'].max()],
                marks={str(int(year)): str(int(year)) for year in tag[tag.tags == default]['YEAR'].unique()},
            ),
            html.Br(),
            dcc.Checklist(tag['TYPE'].unique(), tag['TYPE'].unique(), inline = True, id='DropTypeT'),
        ]),

        html.Br(),
        html.Div([
            dcc.Graph(id="Gtag1"),
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id="Gtag2")
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        html.Div([
            html.H3("Tags commun"),
            dcc.Graph(id="Gtag3")
        ]),
        html.Div([
            html.H3("Auteurs"),
            dcc.Graph(id="Gtag4")
        ]),
        html.Div([
            dcc.Dropdown(aut_db['auteurs'].unique(), "Tous les articles", id='DropDAutTag'),
        ], style = {'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Br(),
            html.Ul(id = "title_p_tag"),
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
                       id = "nb_row"
                       )
        ]),
        html.Div([
            html.H3("Mots les plus fréquents pour ce tag"),
            html.Div(id="table_tag", style={"width" : "50%", "margin": "auto"}),
            html.Br()
        ], style = {'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H3("Mots les plus spécifiques à ce tag"),
            html.Div(id="table_tag_tfidf", style={"width" : "50%","margin": "auto"}),
        ], style = {'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ])
    
])

@callback(
    Output('Gtag1', 'figure'),
    Output("Gtag2", "figure"),
    Output("Gtag3", "figure"),
    Output("Gtag4", "figure"),
    Output("year-sliderT", "min"),
    Output("year-sliderT", "max"),
    Output("year-sliderT", "marks"),
    Output('DropTypeT', "options"),
    Input('DropTag', "value"),
    Input("year-sliderT", "value"),    
    Input('DropTypeT', "value"),
)
def update_Gtag(TAG, year, type):
    min_y = int(year[0])
    max_y = int(year[1])

    #Gaut1
    filtered_df = pd.DataFrame({"values" : tag[tag.tags == TAG][tag.TYPE.isin(type)].YEAR.value_counts().sort_index(),
                                "year" : tag[tag.tags == TAG][tag.TYPE.isin(type)].YEAR.value_counts().sort_index().index})
    
    fig = px.bar(filtered_df, x = "year", y = "values")
    fig.update_layout(transition_duration = 500)
    
    #Gaut2
    filtered_df = pd.DataFrame({"values" : tag[tag.tags == TAG][tag.YEAR >= min_y][tag.YEAR <= max_y].TYPE.value_counts().sort_index(), 
                                "type" : tag[tag.tags == TAG][tag.YEAR >= min_y][tag.YEAR <= max_y].TYPE.value_counts().sort_index().index})
    
    fig2 = px.bar(filtered_df, x = "type", y = "values", color="type")
    fig2.update_layout(transition_duration = 500, showlegend=False)
    
    #Gaut3
    filtered_df = net[net.source == TAG].sort_values(by="values")
    fig3 = px.bar(filtered_df, x = "target", y = "values")
    fig3.update_layout(transition_duration = 500, showlegend=False, xaxis={'categoryorder':'total descending'})
    
    # #Gaut4
    filtered_df = tag_link[tag_link.target == TAG].sort_values(by="values")
    fig4 = px.bar(filtered_df, x = "source", y = "values")
    fig4.update_layout(transition_duration = 500, showlegend=False, xaxis={'categoryorder':'total descending'})
    
    #Slider
    filtered_df = tag[tag.tags == TAG]
    min = filtered_df.YEAR.min()
    max = filtered_df.YEAR.max()
    marks = {}
    for year in tag[tag.tags == TAG]['YEAR'].unique():
        marks[str(int(year))] = str(int(year))

    #Dropdown_type
    options = tag[tag.tags == TAG].TYPE.unique()

    return(fig, fig2, fig3, fig4, min, max, marks, options)

@callback(
    Output("title_p_tag", "children"),
    Output("DropDAutTag", "options"),
    # Output('DropAutTag', "options"),
    Input("DropDAutTag", "value"),
    Input('DropTag', "value"),
    # Input("DropAutTag", "value")
)
def title_tag(aut, tag_input): #, sub_aut):

    urls = tag[tag.tags == tag_input]["Unnamed: 0"]
    tmp = aut_db[aut_db.index.isin(urls)]
    options_auts = np.append(tmp.auteurs.unique(), "Tous les articles")
    # options_aut = np.append(net[net.source == auteur].target.unique(), "Tous les auteurs")
    if aut == "Tous les articles":
        urls = tmp.url.unique()
    else:
        tmp = tmp[tmp.auteurs == aut]
        urls = tmp.url.unique()
    # if sub_aut == 'Tous les auteurs':
    #     pass
    # else:

    #     pass
    data = pd.read_csv("./data/data_article_clean.csv")
    text = data[data.URL.isin(urls)].TITRE

    text = [html.Li(html.A(titre, href=data[data.TITRE == titre].URL.values[0], target="_blank")) for titre in text]

    return(text, options_auts) #, options_aut)


@callback(
        Output("table_tag", "children"),
        Output("table_tag_tfidf", "children"),
        Input('DropTag', "value"),
        Input('nb_row', "value")
)
def table_aut_gen(tag_input, nb_rows):

    text.get_an_aut_termdoc(tfidf, nOcc, tag_input)
    path = f"./pages/data/Txt/Tags/Occurences/{tag_input}.csv"
    dataframe = pd.read_csv(path)
    dataframe.columns = ["Termes", "Occurences"]

    nb_urls = len(tag[tag.tags == tag_input])
    path_tfidf = f"./pages/data/Txt/Tags/TF_IDF/{tag_input}.csv"
    dataframe_tfidf = pd.read_csv(path_tfidf)
    dataframe_tfidf.columns = ["Termes", "tf-idf"]
    dataframe_tfidf["tf-idf"] = round(dataframe_tfidf["tf-idf"] / nb_urls, 3)

    return(generate_table(dataframe, max_rows=nb_rows), generate_table(dataframe_tfidf, max_rows=nb_rows))

def layout():
    return(html.Div([
        main_div  # adjust width
            ])
    )
