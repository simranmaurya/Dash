import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_ag_grid as dag
import dash_iconify
import dash_mantine_components as dmc
import dash
import plotly.express as px
from datetime import datetime, timedelta, date
from dash import callback_context

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

class Singleton:
    __shared_state = dict()
    df = pd.DataFrame()
    old_df = pd.DataFrame()

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return self.df

    def read_file(self):
        self.df = pd.read_csv("file2.csv")
        self.old_df = self.df.copy()

singleton_instance = Singleton()
singleton_instance.read_file()

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
                                dcc.Graph(id="event-type-bar-chart",style={'width':'50%',"height": "300px"}),
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
                             size="sm",
                            value="",
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
                            size="sm",
                            rightSection=dash_iconify.DashIconify(icon="bi:search"),
                            style={"margin": "10px","width": "100%"},
                        )
                    ],
                    style={"display": "inline-block", "width": "200px"},
                ),
                dbc.Col(
                    [
                        dmc.TextInput(
                            id="filter-WORLD_REGION",
                            placeholder="Filter by WORLD_REGION...",
                            size="sm",
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
                                    style={"width": "95%","margin":"5px"},
                                    clearable=False,
                                ),
                                dmc.DatePicker(
                                    id="end-date-picker",
                                    label="End Date",
                                    style={"width": "95%","margin":"5px"},
                                    clearable=False,
                                ),
                                dbc.Button(
                            "Query",
                            id="query-button",
                            n_clicks=0,
                            size="sm",
                            style={"background-color": "#19249C","float":"right", "margin":"5px"},
                        )

                            ],
                            target="popover-target",
                            trigger="click",
                            id="popover-event"
                        ),
                    ],
                    style={"display": "inline-block", "width": "100px"},
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
                id="event-table",
                #  rowData=singleton_instance.df.to_dict("records"),
                columnDefs=[{"field": i} for i in singleton_instance.df.columns],
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
    print(source, start_date, end_date)
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
        )
        & (data["COUNTRY"].str.contains(country, case=False))
        & (data["WORLD_REGION"].str.contains(world_region, case=False))
    ]
    return filtered_data.to_dict("records")

@app.callback(
   [
        Output("event-table", "rowData"),
    ],
    [
        Input("edited-data-store", "data"),
        Input('filter-SOURCE','value'),
    ]
)
def render_ag_data(edited_data, source_filter):
    singleton_instance = Singleton()
    if edited_data:
        return [edited_data]
    return [singleton_instance.df.to_dict('records')]

@app.callback(
    [
        Output("event-table", "columnDefs"),
        Output("edit-button", "color"),
        Output("edited-data-store", "data"),
    ],
    [
        Input("edit-button", "n_clicks"),
        Input("save-button", "n_clicks"),
        Input("filter-SOURCE", "value"),
        Input("filter-COUNTRY", "value"),
        Input("filter-WORLD_REGION", "value"),
        # Input("start-date-picker", "value"),
        # Input("end-date-picker", "value"),
    ],
    [
        State("event-table", "rowData"),
    ],
    prevent_initial_call=True
)
def update_table(edit_n_clicks, save_n_clicks, source, country, world_region, row_data):
    ctx = callback_context

    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered_id.split(".")[0]

    switch = edit_n_clicks % 2 == 1 if triggered_id == "edit-button" else False
    singleton_instance = Singleton()

    editable_columns = ["SOURCE", "PLANT_ID"]
    column_defs = [
        {
            "field": i,

            "filter": "agTextColumnFilter" if singleton_instance.df[i].dtype == 'object' else "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"] if singleton_instance.df[i].dtype == 'object' else ["apply", "reset"],
                "closeOnApply": True,
            },
            "editable": switch if i in editable_columns else False,
        }
        for i in singleton_instance.df.columns
    ]

    button_color = 'primary' if switch else 'light'

    if triggered_id == "save-button":
        edited_df = pd.DataFrame(row_data)
        singleton_instance.old_df = singleton_instance.df.copy()
        singleton_instance.df = edited_df
        edited_df.to_csv("file2.csv", index=False)
        singleton_instance.old_df.to_csv('old.csv', index=False)
        edited_data_store = edited_df.to_dict("records")
        return column_defs, button_color, edited_data_store

    # Search and filter logic
    filtered_data = query_data(singleton_instance.df, source, country, world_region)
    return column_defs, button_color, filtered_data


@app.callback(
    Output("event-type-bar-chart", "figure"),
    [Input("filter-COUNTRY", "value")],
)
def update_bar_chart(country):
    singleton_instance = Singleton()

    # Count occurrences of each EVENT_TYPE
    event_type_counts = singleton_instance.df["EVENT_TYPE"].value_counts()

    colors = px.colors.qualitative.Set3
    figure = {
        "data": [
            {
                "x": event_type_counts.values,
                "y": event_type_counts.index,
                "type": "bar",
                "orientation": "h",
                "marker": {"color": colors,"border-radius":"5px"},

            }
        ],
        "layout": {
            "title": "Event Type Distribution",
            "xaxis": {"title": "Count", "automargin": True},
            "margin": {"l": 150, "r": 20, "t": 40, "b": 40},
        },
    }

    return figure

@app.callback(
    Output("popover-event", "is_open"),
    Input("query-button", "n_clicks"),
    [State("popover-event", "is_open")],
)
def toggle_popover( query_button_clicks, is_open):
    ctx = callback_context
    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered_id.split(".")[0]

    if  triggered_id == "query-button":
        return not is_open

    return is_open

if __name__ == "__main__":
    app.run_server(debug=True)

