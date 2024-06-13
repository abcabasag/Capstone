# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app

# CSS Styling for the NavLink components
navlink_style = {
    'color': '#fff'
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"
}
banner = 'nctslogo.jpg'

sidebar = html.Div(
    [
        html.Img(src=f'/assets/{banner}', style={'width': '150px', 'height': 'auto', 'margin':'auto', 'display': 'block'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/" or "/home", active="exact"),
                dbc.NavLink("Check Request Status", href="/check_request_home" or "/functions/check_request_cc" or "/functions/check_request_vdr", active="exact"),
                dbc.NavLink("Contact Us", href="/contactus", active="exact"),
                dbc.NavLink("Sign up", href="/signup", active="exact"),
                dbc.NavLink("Login", href="/login", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

adminloginsidebar = html.Div(
    [
        html.Img(src=f'/assets/{banner}', style={'width': '150px', 'height': 'auto', 'margin':'auto', 'display': 'block'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/user", active="exact"),
                dbc.NavLink("Procurement", href="/procurement_list" or "/functions/procurement", active="exact"),
                dbc.NavLink("Vehicle Dispatch List", href="/view_request", active="exact"),
                dbc.NavLink("Citizen Charter Request List", href="/view_cc_list", active="exact"),
                dbc.NavLink("Sign up", href="/signup", active="exact"),
                dbc.NavLink("Logout", href="/logout", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

loginsidebar = html.Div(
    [
        html.Img(src=f'/assets/{banner}', style={'width': '150px', 'height': 'auto', 'margin':'auto', 'display': 'block'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Account", href="/user", active="exact"),
                dbc.NavLink("Procurement", href="/procurement_list" or "/functions/procurement", active="exact"),
                dbc.NavLink("Vehicle Dispatch List", href="/view_request", active="exact"),
                dbc.NavLink("Citizen Charter Request List", href="/view_cc_list", active="exact"),
                dbc.NavLink("Logout", href="/logout", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
