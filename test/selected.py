import dash_ag_grid as dag
from dash import Dash, Input, Output, State, callback, dcc, html

app = Dash(__name__)

app.layout = html.Div([
    dag.AgGrid(
    id='ag-grid',
    columnDefs=[
        {'field': 'id'},
        {'field': 'name'},
        # Add more columns as needed
    ],
    rowData=[
        {'id': 1, 'name': 'John'},
        {'id': 2, 'name': 'Jane'},
        # Add more data as needed
    ],
    dashGridOptions={"rowSelection":"multiple"},
)
,
    html.Div(id='selected-rows-output')
])



@app.callback(
    Output('selected-rows-output', 'children'),
    Input('ag-grid', 'selectedRows'),
    prevent_initial_call=True
)
def display_selected_rows(selected_rows):
    if selected_rows:
        return f'Selected Rows: {selected_rows}'
    else:
        return 'No rows selected'

if __name__ == '__main__':
    app.run_server(debug=True)
