from dash import Dash, html, dcc, callback
import dash
# import dash_core_components as dcc 
# import dash_html_components as html 
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path="/")

df = pd.read_csv("data/data_article_clean.csv")

def graph_time():
    
    filtered_df = pd.DataFrame({"values" : df.YEAR.value_counts().sort_index(),
                       "year" : df.YEAR.value_counts().sort_index().index})
    fig = px.area(filtered_df, x="year", y="values")
    return(fig)

def graph_tag_nb():

    tag = pd.read_csv("./res/tags.csv", index_col=0)
    tmp = tag.set_index("url").join(df.set_index("URL")[["YEAR", "DATE", "TYPE"]])
    tmp = tmp.loc[tmp.DATE.notna()] 
    tmp = tmp.groupby("tags").filter(lambda x:len(x) >= 5)
    filtered_df = pd.DataFrame({"values" : tmp.tags.value_counts().sort_index(),
                       "year" : tmp.tags.value_counts().sort_index().index})

    fig = px.bar(filtered_df, x="year", y="values")
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})

    return(fig)

def graph_tag_time():

    tag = pd.read_csv("./res/tags.csv", index_col=0)
    tmp = tag.set_index("url").join(df.set_index("URL")[["YEAR", "DATE", "TYPE"]])
    tmp = tmp.loc[tmp.DATE.notna()]
    filtered_tmp = tmp.groupby("tags").filter(lambda x:len(x) >= 5)
    filtered_tmp.YEAR = filtered_tmp.YEAR.replace([1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1998, 1999], 
                                            "1990-1999").replace([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009], 
                                                            "2000-2009").replace([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019], 
                                                                            "2010-2019").replace([2020, 2021, 2022, 2023, 2024, 2025], "2020-2029")
    temp = pd.crosstab(filtered_tmp.tags, filtered_tmp.YEAR)
    temp = temp.melt(ignore_index=False)
    temp["tag"] = temp.index
    temp = temp.sort_values(by="value")

    fig = px.bar(temp, x="tag", y="value", color="YEAR")
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})

    return(fig)

main_div = html.Div([
    html.Br(),
    html.H2("Ceci est un site d'analyse pour les données récoltées du site Millénaire 3"),
    html.P("Cette page est en cours de réalisation"),
    html.Br(),
    html.Div([
        html.H3("Courbe des productions dans le temps"),
        dcc.Graph(figure=graph_time(), id="GgenTime"),
        html.Br(),
    ]),
    html.Div([
        html.H3("Informations relatives aux tags"),
        html.H5("Nombre de tags"),
        dcc.Graph(figure=graph_tag_nb(), id="GgenTagNB")
    ]),
    html.Div([
        html.H5("Tags dans le temps"),
        dcc.Graph(figure=graph_tag_time())
    ])#, style = {'width': '49%', 'display': 'inline-block'})
])

# @callback(
#         Output("GgenTime", "figure"),
#         Input()
# )


def layout():

    return(main_div)