import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_ag_grid as dag
import dash_iconify
import dash_mantine_components as dmc
import dash
from datetime import datetime, timedelta, date
from dash import callback_context

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

refinery_data = pd.read_csv("file2.csv")


app.layout = html.Div(
    [
        dbc.Row(
            dmc.Accordion(
                chevron=dash_iconify.DashIconify(icon="ant-design:plus-outlined"),
                disableChevronRotation=True,
                children=[
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(
                                "Events Summary",
                                style={"color": "#19249C"},
                            ),
                            dmc.AccordionPanel(
                                "Colors, fonts, shadows and many other parts are customizable to fit your design needs"
                            ),
                        ],
                        value="customization",
                        style={"background-color": "#19249C1A", "border-radius": "5px"},
                    ),
                ],
            ),
            style={"margin": 10},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dmc.TextInput(
                            id="filter-SOURCE",
                            placeholder="Filter by SOURCE...",
                            rightSection=dash_iconify.DashIconify(icon="bi:search"),
                            style={"margin": "10px"},
                        )
                    ],
                    style={"display": "inline-block", "width": "100px"},
                ),
                dbc.Col(
                    [
                        dmc.TextInput(
                            id="filter-COUNTRY",
                            placeholder="Filter by COUNTRY...",
                            rightSection=dash_iconify.DashIconify(icon="bi:search"),
                            style={"margin": "10px"},
                        )
                    ],
                    style={"display": "inline-block", "width": "100px"},
                ),
                dbc.Col(
                    [
                        dmc.TextInput(
                            id="filter-WORLD_REGION",
                            placeholder="Filter by WORLD_REGION...",
                            rightSection=dash_iconify.DashIconify(icon="bi:search"),
                            style={"margin": "10px"},
                        )
                    ],
                    style={"display": "inline-block", "width": "100px"},
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            dash_iconify.DashIconify(icon="uil:calender"),
                            id="popover-target",
                            color="light",
                            style={"margin": "10px"},
                        ),
                        dbc.Popover(
                            [
                                dmc.DatePicker(
                                    id="start-date-picker",
                                    label="Start Date",
                                    style={"width": "100%"},
                                    clearable=False,
                                ),
                                dmc.DatePicker(
                                    id="end-date-picker",
                                    label="End Date",
                                    style={"width": "100%"},
                                    clearable=False,
                                ),
                            ],
                            target="popover-target",
                            trigger="click",
                        ),
                    ],
                    style={"display": "inline-block", "width": "100px"},
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Apply",
                            id="apply-button",
                            n_clicks=0,
                            style={"background-color": "#19249C"},
                        )
                    ],
                    style={"display": "inline-block", "margin": "10px"},
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            dash_iconify.DashIconify(icon="tdesign:edit"),
                            id="edit-button",
                            n_clicks=0,
                            color="light",
                            style={
                                "float": "right",
                                "margin-right": "10px",
                                "margin": "10px",
                            },
                        )
                    ]
                ),
                dbc.Col(
                    dbc.Button("Save", id="save-button", n_clicks=0, className="btn btn-primary"),
                    width="auto",style={
                                "margin": "10px",
                            },
                ),
            ],
            style={
                "backgroundColor": "#EDEDED",
                "marginRight": "1px",
                "marginLeft": "1px",
            },
        ),
        dcc.Store(id="edited-data-store", storage_type="memory"),
        dbc.Row(

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
                    "pagination": True,
                    "paginationPageSize": 20,
                },
                columnSize="sizeToFit",
                style={"height": 600},
            ),
        ),
    ],
    style={"margin": 10},
)


def query_data(
    data, source=None, country=None, world_region=None, start_date=None, end_date=None
):
    data["EVENT_START_DATE"] = pd.to_datetime(data["EVENT_START_DATE"])
    data["EVENT_END_DATE"] = pd.to_datetime(data["EVENT_END_DATE"])

    if start_date and end_date:
        start_date, end_date = pd.Timestamp(start_date, tz="UTC"), pd.Timestamp(
            end_date, tz="UTC"
        )
        data = data[
            (data["EVENT_START_DATE"] >= start_date)
            & (data["EVENT_END_DATE"] <= end_date)
        ]

    filtered_data = data[
        (
            data["SOURCE"].str.contains(source, case=False)
            | data["CITY"].str.contains(source, case=False)
        )
        & (data["COUNTRY"].str.contains(country, case=False))
        & (data["WORLD_REGION"].str.contains(world_region, case=False))
    ]
    return filtered_data.to_dict("records")

@app.callback(
    [
        Output("master-table", "columnDefs"),
        Output("edit-button", "color"),
        Output("edited-data-store", "data"),
        Output("master-table", "rowData"),
    ],
    [
        Input("edit-button", "n_clicks"),
        Input("save-button", "n_clicks"),
        Input("apply-button", "n_clicks"),
    ],
    [
        State("master-table", "rowData"),
        State("filter-SOURCE", "value"),
        State("filter-COUNTRY", "value"),
        State("filter-WORLD_REGION", "value"),
        State("start-date-picker", "value"),
        State("end-date-picker", "value"),
    ],
    prevent_initial_call=True
)
def update_table(edit_n_clicks, save_n_clicks, apply_n_clicks, row_data, source, country, world_region, start_date, end_date):
    ctx = callback_context

    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered_id.split(".")[0]

    switch = edit_n_clicks % 2 == 1 if triggered_id == "edit-button" else False

    editable_columns = ["SOURCE", "PLANT_ID"]
    column_defs = [
        {
            "field": i,
            "filter": "agTextColumnFilter" if refinery_data[i].dtype == 'object' else "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"] if refinery_data[i].dtype == 'object' else ["apply", "reset"],
                "closeOnApply": True,
            },
           "editable": switch if i in editable_columns else False,
        }
        for i in refinery_data.columns
    ]

    button_color = 'primary' if switch else 'light'

    if triggered_id == "save-button":
        edited_df = pd.DataFrame(row_data)
        edited_df.to_csv("file2.csv", index=False)
        edited_data_store = edited_df.to_dict("records")
        return column_defs, button_color, edited_data_store, edited_data_store

    # Search and filter logic
    if triggered_id == "apply-button":
        filtered_data = query_data(refinery_data, source, country, world_region, start_date, end_date)
        return column_defs, button_color, filtered_data, filtered_data

    return column_defs, button_color, dash.no_update, row_data

if __name__ == "__main__":
    app.run_server(debug=True)
