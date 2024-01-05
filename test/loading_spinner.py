import dash
from dash import html, dcc, callback, Output, Input, State
from dash import callback_context,no_update
import time

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button('Open Modal', id='open-modal-btn'),
    
    # Modal
    html.Div([
        html.Div([
            html.Span('Close', id='close-modal-btn', n_clicks=0),
            html.Button('Save', id='save-btn'),
            dcc.Loading(id="loading", type="circle"),
        ], className='modal-content'),
    ], id='modal', style={'display': 'none'}),
])


@app.callback(
    [Output('modal', 'style'),
     Output('loading', 'children')],
    [Input('open-modal-btn', 'n_clicks'),
     Input('close-modal-btn', 'n_clicks'),
     Input('save-btn', 'n_clicks')],
    [State('modal', 'style')]
)
def toggle_modal(open_clicks, close_clicks,save_clicks, current_style):
    ctx = callback_context

    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate
    

    triggered_id = ctx.triggered_id.split(".")[0]
    if triggered_id == "save-btn":
        time.sleep(15)
        return {'display': 'none'},''
    elif open_clicks > 0:
        return {'display': 'block'}, ''
    elif close_clicks > 0:
        return {'display': 'none'}, ''
    


# @app.callback(
#     Output('loading', 'children'),
#     [Input('save-btn', 'n_clicks')]
# )
# def simulate_loading(save_clicks):
#     if save_clicks > 0:
#         time.sleep(5)
#         return ''


if __name__ == '__main__':
    app.run_server(debug=True)
