import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    [
        dbc.Button("Toggle Collapse", id="collapse-button", color="primary"),
        dbc.Row(
            dbc.Col(
                dbc.Collapse(
                    dbc.Card(
                        dbc.CardBody(
                            [

                                            dbc.Button(
                                                "Save", color="primary", size="sm",style={'margin-right':'2px'}
                                            ),

                                            dbc.Button(
                                                "Cancel", color="secondary", size="sm"
                                            )

                            ]
                        ),
                        style={"width": "149px"},
                    ),
                    id="collapse",
                    is_open=False,
                ),
                width=3,  # Adjust the width as needed
                style={
                    "position": "absolute",
                    "top": "10px",
                    "right": "1000px",
                },  # Positioning
            ),
        ),
    ]
)


@app.callback(
    dash.dependencies.Output("collapse", "is_open"),
    [dash.dependencies.Input("collapse-button", "n_clicks")],
)
def toggle_collapse(n):
    return (n or 0) % 2 == 1


if __name__ == "__main__":
    app.run_server(debug=True)
