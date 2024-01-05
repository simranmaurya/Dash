from dash import Dash, html, Input, Output, callback
import dash_bootstrap_components as dbc

user_field = ['Latitude','Longitude','Data','Country']

simulation_layout = html.Div([html.H2('User Field'),
                            html.Br(),
                            html.Div([
                                html.Tr([
                                    html.Td(html.H5(value,style={'width':'150px'})),
                                    html.Td(html.P('0',style={'width':'150px','padding-left':'5px','color':'white','background-color':'#728a79','text-align':'center'}))
                                ])
                                for value in user_field
                            ])
                        ],style={'padding-left':'20px'})


