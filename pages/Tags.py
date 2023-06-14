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
tag_link = pd.read_csv("./pages/data/tag2aut.csv")
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
            dcc.Graph(id="Gtag3")
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id="Gtag4")
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
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
    filtered_df = net[net.source == TAG]
    fig3 = px.bar(filtered_df, x = "target", y = "values")
    fig3.update_layout(transition_duration = 500, showlegend=False)
    
    # #Gaut4
    filtered_df = tag_link[tag_link.source == TAG]
    fig4 = px.bar(filtered_df, x = "target", y = "values")
    fig4.update_layout(transition_duration = 500, showlegend=False)
    
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

def layout():
    return(html.Div([
        main_div  # adjust width
            ])
    )
