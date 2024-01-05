import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
import dash_ag_grid as dag
import dash_daq as daq
import dash_iconify
import dash_mantine_components as dmc
import dash
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

refinery_data = pd.read_csv("file2.csv")

app.layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dmc.TextInput(
                    id='filter-Cotinent',
                    placeholder='Search ...',
                    rightSection=dash_iconify.DashIconify(icon="bi:search"),
                    style={'width': '200px'}
                )
            ], style={'display': 'inline-block'}),
            dbc.Col([
                dbc.Button(
                    dash_iconify.DashIconify(icon="tdesign:edit"),
                    id="edit-button",
                    n_clicks=0,
                    color='light',
                    style={'float': 'right', 'margin-right': '10px', 'margin-bottom': '10px'}
                )
            ])
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


@app.callback(
    [
        Output("master-table", "columnDefs"),
        Output("edit-button", "color"),
    ],
    [Input("edit-button", "n_clicks")]
)
def toggle_edit_mode(n_clicks):
    if n_clicks is None:
        switch = False
    else:
        switch = n_clicks % 2 == 1
    print(switch)
    editable_columns = ["REFINERY_NAME", "AMPOL_REFINERY_ID", "OPER_NAME", "OWNER_NAME", "PARENT_NAME"]
    column_defs = [
        {
            "field": i,
            "filter": "agTextColumnFilter" if refinery_data[i].dtype == 'object' else "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"] if refinery_data[i].dtype == 'object' else ["apply", "reset"],
                "closeOnApply": True,
            },
            "editable": switch
        }
        for i in refinery_data.columns
    ]

    button_color = 'primary' if switch else 'light'

    return column_defs, button_color



if __name__ == "__main__":
    app.run_server(debug=True)