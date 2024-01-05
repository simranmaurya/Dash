import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State
from views import about_page as vw_ap
from views import input_page as vw_ip
from views import simulation as vw_sim
from views import logout as vw_log

app = Dash(external_stylesheets = [dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

nav_list = [('About',''),
            ('Input','input_page'),
            ('Simulation','simulation'),
            ('Logout','logout')]

nav_bar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(val[0],href='/'+val[1],style = {'color':'white'})) for val in nav_list],
    brand="DASH APP",
    brand_href="/",
    color="primary",
    dark=True,
)

page_content = html.Div(id='page-content')

app.layout = html.Div([dcc.Location(id="url"), nav_bar, page_content])

@app.callback(Output(component_id = 'page-content',component_property = 'children'),
              Input(component_id = 'url',component_property = 'pathname'))
def get_content(pathname):
    if pathname == '/':
        return vw_ap.about_page_layout
    elif pathname == '/input_page':
        return vw_ip.input_page_layout
    elif pathname == '/simulation':
        return vw_sim.simulation_layout
    else:
        return vw_log.logout_layout

if __name__ == '__main__':
    app.run_server(debug = True)