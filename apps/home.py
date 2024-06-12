# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app
from apps import dbconnect as db
from urllib.parse import urlparse, parse_qs

# Define styles
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

layout = html.Div(
    [
        html.H2('UP NCTS Request Portal', style=WELCOME_TEXT_STYLE),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.CardImg(
                                            src="/assets/cc_logo.png",
                                            className="img-fluid rounded-start",
                                        ),
                                        className="col-md-4",
                                    ),
                                    dbc.Col(
                                        dbc.CardBody(
                                            [
                                                html.H4("Citizen Charter Request", className="card-title"),
                                                html.P(
                                                    "Request based on the 18 Citizen Charter Services by UP NCTS",
                                                    className="card-text",
                                                ),
                                                dbc.Button("Request for Citizen Charter Service", href="/functions/firstpage_cc", color="primary"),
                                            ]
                                        ),
                                        className="col-md-8",
                                    ),
                                ],
                                className="g-0 d-flex align-items-center",
                            )
                        ],
                        className="mb-3",
                        style={"maxWidth": "700px"},
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.CardImg(
                                            src="/assets/vd_logo.png",
                                            className="img-fluid rounded-start",
                                        ),
                                        className="col-md-4",
                                    ),
                                    dbc.Col(
                                        dbc.CardBody(
                                            [
                                                html.H4("Vehicle Dispatch Request", className="card-title"),
                                                html.P(
                                                    "Request to borrow one of the 5 vehicles offered by UP NCTS",
                                                    className="card-text",
                                                ),
                                                dbc.Button("Borrow a vehicle", href="/functions/firstpage_vdr", color="primary"),
                                            ]
                                        ),
                                        className="col-md-8",
                                    ),
                                ],
                                className="g-0 d-flex align-items-center",
                            )
                        ],
                        className="mb-3",
                        style={"maxWidth": "700px"},
                    ),
                ),
            ],
            style={"margin-bottom": "40px"},
        ),
        html.Div(
            [
                html.Span(
                    "A web-based application to request a service to UP NCTS.",
                    style=INFO_TEXT_STYLE
                ),
                html.Br(),
                html.Br(),
                html.Span(
                    "Contact the owner if you need assistance!",
                    style=ITALIC_TEXT_STYLE
                ),
            ]
        )
    ],
    style={'max-width': '1500px', 'margin-left': '220px'},  # Center the content and set a maximum width
)# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app
from apps import dbconnect as db
from urllib.parse import urlparse, parse_qs

# Define styles
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

layout = html.Div(
    [
        html.H2('UP NCTS Request Portal', style=WELCOME_TEXT_STYLE),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.CardImg(
                                            src="/assets/cc_logo.png",
                                            className="img-fluid rounded-start",
                                        ),
                                        className="col-md-4",
                                    ),
                                    dbc.Col(
                                        dbc.CardBody(
                                            [
                                                html.H4("Citizen Charter Request", className="card-title"),
                                                html.P(
                                                    "Request based on the 18 Citizen Charter Services by UP NCTS",
                                                    className="card-text",
                                                ),
                                                dbc.Button("Request for Citizen Charter Service", href="/functions/firstpage_cc", color="primary"),
                                            ]
                                        ),
                                        className="col-md-8",
                                    ),
                                ],
                                className="g-0 d-flex align-items-center",
                            )
                        ],
                        className="mb-3",
                        style={"maxWidth": "700px"},
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.CardImg(
                                            src="/assets/vd_logo.png",
                                            className="img-fluid rounded-start",
                                        ),
                                        className="col-md-4",
                                    ),
                                    dbc.Col(
                                        dbc.CardBody(
                                            [
                                                html.H4("Vehicle Dispatch Request", className="card-title"),
                                                html.P(
                                                    "Request to borrow one of the 5 vehicles offered by UP NCTS",
                                                    className="card-text",
                                                ),
                                                dbc.Button("Borrow a vehicle", href="/functions/firstpage_vdr", color="primary"),
                                            ]
                                        ),
                                        className="col-md-8",
                                    ),
                                ],
                                className="g-0 d-flex align-items-center",
                            )
                        ],
                        className="mb-3",
                        style={"maxWidth": "700px"},
                    ),
                ),
            ],
            style={"margin-bottom": "40px"},
        ),
        html.Div(
            [
                html.Span(
                    "A web-based application to request a service to UP NCTS.",
                    style=INFO_TEXT_STYLE
                ),
                html.Br(),
                html.Br(),
                html.Span(
                    "Contact the owner if you need assistance!",
                    style=ITALIC_TEXT_STYLE
                ),
            ]
        )
    ],
    style={'max-width': '1500px', 'margin-left': '220px'},  # Center the content and set a maximum width
)
