import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output,State
import dash_ag_grid as dag
import dash_iconify
import dash_mantine_components as dmc
import dash
from datetime import datetime, timedelta, date

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

refinery_data = pd.read_csv("file2.csv")

app.layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dmc.TextInput(
                    id='filter-SOURCE',
                    placeholder='Filter by SOURCE...',
                    rightSection=dash_iconify.DashIconify(icon="bi:search"),
                    style={'width': '200px'}
                )
            ], style={'display': 'inline-block'}),
            dbc.Col([
                dmc.TextInput(
                    id='filter-COUNTRY',
                    placeholder='Filter by COUNTRY...',
                    rightSection=dash_iconify.DashIconify(icon="bi:search"),
                    style={'width': '200px'}
                )
            ], style={'display': 'inline-block'}),
            dbc.Col([
                dmc.TextInput(
                    id='filter-WORLD_REGION',
                    placeholder='Filter by WORLD_REGION...',
                    rightSection=dash_iconify.DashIconify(icon="bi:search"),
                    style={'width': '200px'}
                )
            ], style={'display': 'inline-block'}),
            dbc.Col([
                dmc.DateRangePicker(
                    id='date-range-picker',
                    allowSingleDateInRange=True,
                    initialLevel='date',
                    clearable=True,
                    fullWidth=True,
                    style={'width': '200px'}
                )
            ], style={'display': 'inline-block'}),
            dbc.Col([
                dbc.Button("Apply", id="apply-button", n_clicks=0, color='primary')
            ], style={'display': 'inline-block'}),
        ]),

        dag.AgGrid(
            id="master-table",
            rowData=refinery_data.to_dict("records"),
            columnDefs=[{"field": i} for i in refinery_data.columns],
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

def query_data(data, source=None, country=None, world_region=None, date_range=None):
    # Convert EVENT_START_DATE and EVENT_END_DATE to datetime
    data['EVENT_START_DATE'] = pd.to_datetime(data['EVENT_START_DATE'])
    data['EVENT_END_DATE'] = pd.to_datetime(data['EVENT_END_DATE'])

    
    if date_range and len(date_range) == 2:
        start_date, end_date = pd.Timestamp(date_range[0], tz='UTC'), pd.Timestamp(date_range[1], tz='UTC')
        data = data[
            (data['EVENT_START_DATE'] >= start_date) &
            (data['EVENT_END_DATE'] <= end_date)
        ]

    filtered_data = data[
        (data['SOURCE'].str.contains(source, case=False)) &
        (data['COUNTRY'].str.contains(country, case=False)) &
        (data['WORLD_REGION'].str.contains(world_region, case=False))
    ]
    return filtered_data.to_dict("records")



@app.callback(
    Output("master-table", "rowData"),
    [
        Input("apply-button", "n_clicks"),
    ],
    [
        State("filter-SOURCE", "value"),
        State("filter-COUNTRY", "value"),
        State("filter-WORLD_REGION", "value"),
        State("date-range-picker", "value"),
    ]
)
def update_table(n_clicks, source, country, world_region, date_range):
    print(date_range,)
    if n_clicks > 0 and (source, country, world_region, date_range) !=0:
        filtered_data = query_data(refinery_data, source, country, world_region, date_range)
        return filtered_data
    else:
        return refinery_data.to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)
