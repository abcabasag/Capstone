from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db

import dash
import dash_html_components as html
import dash_leaflet as dl

# Coordinates from Google Maps
latitude = 14.656961217311753
longitude = 121.07009927489715

WELCOME_TEXT_STYLE = {
    'font-size': '2.5em',
    'color': '#007BFF',
}

INFO_TEXT_STYLE = {
    'font-size': '1.2em',
}

ITALIC_TEXT_STYLE = {
    'font-style': 'italic',
}

# App layout
layout = html.Div([
    dl.Map(center=[latitude, longitude], zoom=25, children=[
        dl.TileLayer(),
        dl.Marker(position=[latitude, longitude], children=[
            dl.Tooltip("UP National Center for Transportation Studies"),
            dl.Popup([
                html.H1("UP National Center for Transportation Studies"),
                html.P("G. Apacible Street, Diliman, Quezon City, 1101 Metro Manila")
            ])
        ])
    ], style={'width': '100%', 'height': '500px'}),
    html.Br(),  # Inserting a line break for spacing
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.Row([
                    dbc.Col(
                        dbc.CardBody([
                            html.H4("Email Address", className="card-title"),
                            html.P("upncts@up.edu.ph", className="card-text"),
                        ]),
                        className="col-md-8",
                    ),
                ], className="g-0 d-flex align-items-center"),
                className="mb-3",
                style={"maxWidth": "450px"},
            ),
        ], width=4),  # Specify width for the column
        dbc.Col([
            dbc.Card(
                dbc.Row([
                    dbc.Col(
                        dbc.CardBody([
                            html.H4("Contact Number", className="card-title"),
                            html.P("Telephone Number: (02) 8929-4403 / (02) 8981-8500 local 3551", className="card-text"),
                        ]),
                        className="col-md-8",
                    ),
                ], className="g-0 d-flex align-items-center"),
                className="mb-3",
                style={"maxWidth": "450px"},
            ),
        ], width=4),  # Specify width for the column
        dbc.Col([
            dbc.Card(
                dbc.Row([
                    dbc.Col(
                        dbc.CardBody([
                            html.H4("Address", className="card-title"),
                            html.P("UP NCTS, G. Apacible Street, Diliman, Quezon City, 1101 Metro Manila", className="card-text"),
                        ]),
                        className="col-md-8",
                    ),
                ], className="g-0 d-flex align-items-center"),
                className="mb-3",
                style={"maxWidth": "450px"},
            ),
        ], width=4)  # Specify width for the column
    ])
], style={'max-width': '1500px', 'margin-left': '220px'},
)
