from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
from urllib.parse import urlparse, parse_qs

input_style = {
    "border": "1px solid #0056b3",
    "border-radius": "4px",
    "width": "100%",
    "height": "38px"  # Ensures all input fields have the same height
}

# Define the layout
layout = html.Div(
    [
        dbc.Button(
            html.Img(src='/assets/back.svg'),
            id='back_button',
            href='/home',  # Adjust this URL to match your home page URL
            outline=True,
            color="light",
            style={"margin-bottom": "10px"}  # Add some space below the button
        ),
        html.H2('Vehicle Dispatch Request', style={"color": "#0056b3"}),  # Page Header with blue color
        html.Hr(),
        dbc.Alert(id='fp_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label("Full Name", style={"color": "#0056b3"}), width=2  # Label with blue color
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='first_name',
                                placeholder='First Name',
                                style=input_style 
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='middle_initial',
                                placeholder='M.I.',
                                style=input_style 
                            ),
                            width=1,
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='last_name',
                                placeholder='Last Name',
                                style=input_style
                            ),
                            width=3,
                        ),
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label("Unit / Organization", style={"color": "#0056b3"}), width=2  # Label with blue color
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='unit_organization',
                                placeholder='Unit / Organization',
                                style=input_style
                            ),
                            width=3,
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label("Email Address", style={"color": "#0056b3"}), width=2  # Label with blue color
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='email',  # Changed to dbc.Input for consistency
                                id='vdr_email',
                                placeholder='user@example.com',
                                style=input_style  # Blue border, rounded corners, and uniform height for input
                            ),
                            width=3,
                        ),
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label("Contact Number", style={"color": "#0056b3"}), width=2  # Label with blue color
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',  # Changed to dbc.Input for consistency
                                id='vdr_number',
                                placeholder='Input mobile number here',
                                style=input_style  # Blue border, rounded corners, and uniform height for input
                            ),
                            width=3,
                        ),
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                'Next',
                                id='fp_submit',
                                href="/functions/vehicledispatchrequest",
                                n_clicks=0,
                                disabled=True,  # Initially disable the button
                                color="primary",  # Blue button
                                style={"width": "100%"}  # Make the button full width
                            ),
                            width={"size": 2, "offset": 5}
                        )
                    ]
                )
            ]
        ),
    ],
    style={"maxWidth": "1600px", "margin-left": "220px"}
)

# Callback to enable/disable the submit button based on form completeness
@app.callback(
    Output('fp_submit', 'disabled'),
    [
        Input('first_name', 'value'),
        Input('last_name', 'value'),
        Input('unit_organization', 'value'),
        Input('vdr_email', 'value'),
        Input('vdr_number', 'value'),
    ]
)
def toggle_submit_button(first_name, last_name, unit_organization, vdr_email, vdr_number):
    if all([first_name, last_name, unit_organization, vdr_email, vdr_number]):
        return False
    return True


@app.callback(
    [
        Output('fp_alert', 'color'),
        Output('fp_alert', 'children'),
        Output('fp_alert', 'is_open')
    ],
    [
        Input('fp_submit', 'n_clicks')
    ],
    [
        State('first_name', 'value'),
        State('middle_initial', 'value'),
        State('last_name', 'value'),
        State('unit_organization', 'value'),
        Input('vdr_email', 'value'),
        Input('vdr_number', 'value'),
    ]
)

def fp_saveprofile(submitbtn,
                   first_name,
                   middle_initial,
                   last_name,
                   unit_organization,
                   vdr_email,
                   vdr_number):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'fp_submit' or not submitbtn:
        raise PreventUpdate

    alert_open = False
    alert_color = ''
    alert_text = ''

    if not all([first_name, last_name, unit_organization, vdr_email, vdr_number]):
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please supply all required information.'
    else:
        try:
            sql = '''
                INSERT INTO request_class (rc_first_name, rc_middle_i, rc_last_name, organization, email, contact_number, request_class_delete)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            values = [first_name, middle_initial, last_name, unit_organization, vdr_email, vdr_number, False]
            db.modifydatabase(sql, values)
        except Exception as e:
            alert_open = True
            alert_color = 'danger'
            alert_text = f"An error occurred: {str(e)}"

    return alert_color, alert_text, alert_open
