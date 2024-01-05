import pandas as pd
import json
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
from dash import Dash, dcc,html, Input, Output, State, callback

country_df = pd.read_csv('assests/gapminder_full.csv')
features = country_df.columns

with open ("core/conf/config_about.json") as file:
    about_table = json.load(file)

about_page_layout = html.Div([dbc.Row(html.H1(about_table["intro_line1"],style={'text-align':'center'})),
                                dbc.Row(html.H3(about_table["intro_line2"],style={'padding-left':'20px'})),
                                dbc.Row(html.P(about_table["description"],style={'padding-left':'20px'})),
                                html.Br(),
                                dbc.Label("No of Rows"),
                                dcc.Dropdown(id='page_no',options = [5,10,15,20],value=10),
                                DataTable(id='table',columns = [{"name":i,"id":i} for i in features]),
                                dbc.Row([dbc.Col(dcc.Dropdown(id='continent',options = country_df['continent'].unique(),value = country_df['continent'][0])),
                                        dbc.Col(dcc.Dropdown(id='country',options = country_df['country'].unique(),value = country_df['country'][0]))
                                    ])                         
                              ])
@callback(Output("table", 'data'),
              Output("table", 'page_size'),
         [Input('continent', 'value'),
         Input('country', 'value'),
          Input('page_no', 'value')])
def update_function(continent_v, country_v, page_len):
    df_copy= country_df.copy()
    if continent_v:
        df_copy= df_copy[df_copy['continent']== continent_v]
    if country_v:
        df_copy= df_copy[df_copy['country']== country_v]

    return df_copy.to_dict('records'), page_len
