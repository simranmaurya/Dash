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
from dash import callback_context,no_update
import time
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
flag = True

class Singleton:
    __shared_state = dict()
    df = pd.DataFrame()
    new_df = pd.DataFrame()
    edited_df = pd.DataFrame()

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return self.df

    def read_file(self):
        self.df = pd.read_csv("file2.csv")
        self.new_df = pd.DataFrame()
        self.edited_df = pd.DataFrame()

singleton_instance = Singleton()
singleton_instance.read_file()

app.layout = html.Div(
    [   dmc.LoadingOverlay(
            dbc.Modal(
                [
                dbc.ModalHeader([dbc.Row([
                                        dbc.Col(dbc.ModalTitle("Edit Selected Events",style={'float':'left','margin':'20px'}),),
                                        dbc.Col(dcc.Loading(id="loading", type="circle",fullscreen=True,style={'opacity': 0.5})),
                                        dbc.Col(dbc.Button("Save", id="save-modal-button", n_clicks=0, className="btn btn-primary",
                                            style={'float':'right','margin':'20px','margin-right':'10px'}),)
                                    ],
                                    style={'width':'100%'}
                                )],),
                dbc.ModalBody([
                               dag.AgGrid(id="modal-grid",
                                                        className="ag-theme-alpine font",
                                                        columnDefs=[{"field": i} for i in singleton_instance.df.columns],
                                                        defaultColDef={"minWidth": 100,
                                                                        "editable": True},
                                                        dashGridOptions={'pagination':True,
                                                                         "paginationPageSize": 20,
                                                                         "editType": "fullRow"},
                                                        columnSize="sizeToFit",
                                                        style={"height": 600}
                                                    ),
                                
                            ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close-dismiss", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal-edit",
            size = 'xl',
            is_open=False,
        )),
        #html.Div(id="loading-spinner"),
        #dcc.Loading(dcc.Loading(id="loading", type="circle")),
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
                            [
                             dbc.Row(

                                  )
                             ]
                            ),
                        ],
                        value="customization",
                        style={"background-color": "#19249C1A", "border-radius": "5px"},
                    ),
                ],
            ),
            style={"margin-bottom": 10},
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
                            disabled = flag,
                            color="light",
                            style={
                                "float": "right",
                                "margin-right": "10px",
                                "margin": "10px"
                            },
                        )
                    ]
                ),
                # dbc.Col(
                #     dbc.Button("Save", id="save-button", n_clicks=0, className="btn btn-primary"),
                #     width="auto",style={
                #                 "margin": "10px",
                #             },
                # ),
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
                columnDefs=[{"field": i,"checkboxSelection": True if i == singleton_instance.df.columns[0] else False} for i in singleton_instance.df.columns],
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
                    "rowSelection":"multiple"
                },
                columnSize="sizeToFit",
                style={"height": 600},
            ),
        ),
    ],
    style={"margin": 10},
)


def query_data(
    data, source=None
):
    filtered_data = data[

            data["SOURCE"].str.contains(source, case=False)
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



# @app.callback(
#     Output("modal-edit", "is_open"),
#     [Input("edit-button", "n_clicks"),
#     Input("save-modal-button","n_clicks")],
#     [State("modal-edit", "is_open")],
# )
# def toggle_modal(n1,n2,is_open):
#     if n1 or n2 :
#         return not is_open
#     return is_open

@app.callback(
    [
        Output("event-table", "columnDefs"),
        Output("modal-edit", "is_open"),
        Output("modal-grid", "rowData"),
        Output("loading","is_loading")
    ],
    [
        Input("edit-button", "n_clicks"),
        Input("save-modal-button", "n_clicks"),
        Input("filter-SOURCE", "value"),
        Input("event-table","selectedRows"),
        Input("modal-grid", "rowData")
    ],
    [State("modal-edit", "is_open")],
    prevent_initial_call=True
)
def update_table(edit_n_clicks, save_n_clicks, source,selected_rows, row_data,modal_state):
    ctx = callback_context

    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    

    triggered_id = ctx.triggered_id.split(".")[0]
    switch = edit_n_clicks % 2 == 1 if triggered_id == "edit-button" else False
    # singleton_instance = Singleton()
    editable_columns = ["SOURCE", "PLANT_ID"]
    column_defs = [
        {
            "field": i,
            "checkboxSelection": True if i == singleton_instance.df.columns[0] else False,
            #"checkboxSelection": False,
            "filter": "agTextColumnFilter" if singleton_instance.df[i].dtype == 'object' else "agNumberColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"] if singleton_instance.df[i].dtype == 'object' else ["apply", "reset"],
                "closeOnApply": True,
            },
            "editable": switch if i in editable_columns else False,
        }
        for i in singleton_instance.df.columns
    ]

    #button_color = 'primary' if switch else 'light'
    #button_color = not None if switch else None
    if triggered_id == "save-modal-button":
        singleton_instance.edited_df = pd.DataFrame(row_data)
        time.sleep(5)
        return column_defs ,False ,singleton_instance.edited_df.to_dict("records"), True
    
    if triggered_id == "event-table":
        singleton_instance.new_df = pd.DataFrame(selected_rows)
         #if edit_button["display"] == "none" else {"display": "none"}
        

        return column_defs,False,singleton_instance.new_df.to_dict("records"), False
    
    if triggered_id == "edit-button":
        return column_defs,True,singleton_instance.new_df.to_dict("records"), False
    
    return column_defs,False, pd.DataFrame(selected_rows).to_dict("records"), no_update




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


