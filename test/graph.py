import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


fig1_placeholder = dcc.Graph(id='first-graph', figure={})
fig2_placeholder = dcc.Graph(id='second-graph', figure={})

app.layout =  html.Div([
    html.H4('Analysis of Iris data using scatter matrix'),
    dbc.Button("Show First Graph",id="button1",n_clicks=0),
    dbc.Button("Show Second Graph",id="button2",n_clicks=0),
    html.Div(id='container1', children=[fig1_placeholder]),
    html.Div(id='container2', children=[fig2_placeholder]),
    #html.Div(id='gantt-chart-container', children=[fig_placeholder]),
    #html.Div(id="first-graph"),
    #html.Div(id="second-graph")
])

df = pd.read_csv('file2.csv')
df['EVENT_START_DATE'] = pd.to_datetime(df['EVENT_START_DATE'])
df['CAPACITY_OFFLINE'] = pd.to_numeric(df['CAPACITY_OFFLINE'])


@app.callback(
    [Output("first-graph","figure"),
     Output("second-graph","figure")],
    [Input("button1","n_clicks"),
     Input("button2","n_clicks")]
)
def show_g1(n1,n2):
    ctx = dash.callback_context
    button_id = ctx.triggered_id.split('.')[0] if ctx.triggered_id else None

    if button_id == 'button1':
        fig = px.area(df, x='EVENT_START_DATE', y='CAPACITY_OFFLINE', color='UNIT_TYPE', title='Capacity Offline Over Time')
        return fig,None
    
    elif button_id == 'button2':
        fig = px.timeline(df, x_start='EVENT_START_DATE', x_end='EVENT_END_DATE', y='UNIT_NAME', color='WORLD_REGION',
                  labels={'UNIT_NAME': 'Unit Name', 'EVENT_START_DATE': 'Event Start Date'},
                  title='Gantt Chart of Unit Events')

        fig.update_yaxes(categoryorder='total ascending')
        return None,fig
    
    return None,None

if __name__ == '__main__':
    app.run_server(debug=True)

 