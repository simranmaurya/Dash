import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
import dash
import dash_iconify
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px

df = pd.read_csv('file3.csv')

df['EVENT_START_DATE'] = pd.to_datetime(df['EVENT_START_DATE'])
df['CAPACITY_OFFLINE'] = pd.to_numeric(df['CAPACITY_OFFLINE'])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Button(
            dash_iconify.DashIconify(icon="ic:twotone-add"),
            id="collapse-button",
            color="light",
            n_clicks=0,

        ),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    [
                        dcc.Dropdown(
                            id='unit-dropdown',
                            options=[{'label': unit, 'value': unit} for unit in df['UNIT_TYPE'].unique()],
                            value=['VDU'],
                            multi=True
                        ),
                        dcc.Graph(
                            id='time-series-plot'
                        )
                    ]
                )
            ),
            id="collapse",
            is_open=False,
        ),
    ]
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('time-series-plot', 'figure'),
    [Input('unit-dropdown', 'value')]
)
def update_time_series_plot(selected_units):
    filtered_df = df[df['UNIT_TYPE'].isin(selected_units)]
    fig = px.area(filtered_df, x='EVENT_START_DATE', y='CAPACITY_OFFLINE', color='UNIT_TYPE',
                  title='Capacity Offline Over Time')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
