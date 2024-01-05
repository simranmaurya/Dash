from dash import Dash, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

user_field = ['Latitude','Longitude','Data','Country']

input_page_layout = html.Div([html.Tr([html.Td([
                                html.H2("USER INPUT"),
                                html.Br(), 
                                dbc.Row([dbc.Label("Latitude"),dbc.Input(placeholder="Enter Latitude", type="text",style = {'width':'500px','border':'2px solid #f55742'})]),
                                html.Br(),
                                dbc.Row([dbc.Label("Longitude"),dbc.Input(placeholder="Enter Longitude", type="text",style = {'width':'500px','border':'2px solid #f55742'})]),
                                html.Br(),
                                dbc.Row([dbc.Label("Data"),dbc.Input(placeholder="Enter Data", type="text",style = {'width':'500px','border':'2px solid #f55742'})]),
                                html.Br(),
                                dbc.Row([dbc.Label("Country"),dbc.Input(placeholder="Enter Country", type="text",style = {'width':'500px','border':'2px solid #f55742'})]),
                                html.Br(),
                                html.Br(),
                                dbc.Button("Submit",id='button',color = 'primary',style = {'width':'200px'})
                                ],style = {'padding-left':'20px'}),
                            html.Td([
                                html.H2("OUTPUT"),
                                html.Br(),
                                html.P(id='paragraph')
                            ])
                            ])
])

@callback(Output(component_id='paragraph',component_property='children'),
          Input(component_id='button',component_property='n_clicks')
          )
def button_click(n_clicks):
    if n_clicks is not None:
        return "Output Generated"