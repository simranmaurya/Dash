from dash import Dash, html, Input, Output,callback_context
import dash
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

app = Dash()

row_list = [
            {'name':'Sim','age':'23','home':'BLR'},
            {'name':'Sim','age':'23','home':'BLR'},
            {'name':'Sim','age':'23','home':'BLR'},
            {'name':'Sim','age':'23','home':'BLR'},          
]

col_list = [
            {'field':'name'},
           {'field':'age'},
           {'field':'home'}
]

app.layout = html.Div([
    dag.AgGrid(
        id='ag-grid',
        columnDefs=col_list,
        rowData=row_list,
        defaultColDef={
            "filter":True,
            "floatingFilter":True
        }
    ),
    dbc.Button("Reset",
               id='reset',
               n_clicks=0)

])


@app.callback(
    Output("ag-grid","defaultColDef"),
    Input("reset","n_clicks")
)
def clear_filter(reset_clicks):
    ctx = callback_context

    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    

    triggered_id = ctx.triggered_id.split(".")[0]
    if triggered_id == "reset":
        print("1")
        defaultColDef={"filter":True,"floatingFilter":False}
        print("2")
        return defaultColDef

if __name__ == '__main__':
    app.run_server(debug=True)