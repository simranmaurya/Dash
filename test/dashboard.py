import dash
from dash import Dash, dcc, html, Input, Output
import dash_ag_grid as dag
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


df = pd.read_csv('file2.csv')
df['EVENT_START_DATE'] = pd.to_datetime(df['EVENT_START_DATE'])
df['CAPACITY_OFFLINE'] = pd.to_numeric(df['CAPACITY_OFFLINE'])

fig1 = px.area(df, x='EVENT_START_DATE', y='CAPACITY_OFFLINE', color='UNIT_TYPE', title='Capacity Offline Over Time')
fig2 = px.timeline(df, x_start='EVENT_START_DATE', x_end='EVENT_END_DATE', y='UNIT_NAME', color='WORLD_REGION',
                  labels={'UNIT_NAME': 'Unit Name', 'EVENT_START_DATE': 'Event Start Date'},
                  title='Gantt Chart of Unit Events')

fig2.update_yaxes(categoryorder='total ascending')
                

app.layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                        dbc.CardBody(
                            [
                                html.H4("Figure 2", className="card-title"),
                                dcc.Graph(figure=fig1)
                            ]
                        ),
                    ],
                    style={"backgroundColor":"#EDEDED"},
                )
            ], style={'display': 'inline-block'}),
            dbc.Col([
                dbc.Card([
                        dbc.CardBody(
                            [
                                html.H4("Figure 2", className="card-title"),
                                dcc.Graph(figure=fig2)
                            ]
                        ),
                    ],
                    style={"backgroundColor":"#EDEDED"},
                )
            ], style={'display': 'inline-block'}),
            dbc.Col([
                dbc.Card([
                        dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
                        dbc.CardBody(
                            [
                                html.H4("Card title", className="card-title"),
                                dcc.Graph(figure=fig2)
                            ]
                        ),
                    ],
                    style={"backgroundColor":"#EDEDED"},
                )
            ], style={'display': 'inline-block'}),
            
            
        ]),

        dag.AgGrid(
            id="master-table",
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            defaultColDef={
                "minWidth": 200,
                "filter": True,
                "floatingFilter": True,
                "resizable": True,
                "sortable": True,
                "editable": True,
            },
            dashGridOptions={
                'pagination': True,
                "paginationPageSize": 20,
                "editType": "fullRow",
            },
            columnSize="sizeToFit",
            style={"height": 600},
        ),
    ],
    style={"margin": 20}
)


if __name__ == '__main__':
    app.run_server(debug=True)