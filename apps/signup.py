import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Enter the details'),
        html.Hr(),
        dbc.Alert('Please supply details.', color="danger", id='signup_alert', is_open=False),
        dbc.Alert('Username already exists. Please choose a different username.', color="warning", id='username_exists_alert', is_open=False),
        dbc.Alert('Passwords do not match. Please try again.', color="danger", id='password_mismatch_alert', is_open=False),
        dbc.Row(
            [
                dbc.Label("Full Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id='first_name',
                        placeholder='First Name',
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id='middle_initial',
                        placeholder='M.I.',
                    ),
                    width=1,
                ),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id='last_name',
                        placeholder='Last Name',
                    ),
                    width=2,
                ),
            ],
            className='mb-3'
        ),
        dbc.Row(
            [
                dbc.Label("Username", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_username", placeholder="Enter a username"
                    ),
                    width=5,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_password", placeholder="Enter a password"
                    ),
                    width=5,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(" Confirm Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_passwordconf", placeholder="Re-type the password"
                    ),
                    width=5,
                ),
            ],
            className="mb-3",
        ),
        dbc.Button('Sign up', color="secondary", id='signup_signupbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("User Saved")),
                dbc.ModalBody("User has been saved", id='signup_confirmation'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", href='/user'
                    )
                ),
            ],
            id="signup_modal",
            is_open=False,
        ),
    ],
    style={'max-width': '1500px', 'margin-left': '220px'},
)

# Enable the signup button if all required fields are filled
@app.callback(
    [
        Output('signup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_username', 'value'),
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
        Input('first_name', 'value'),
        Input('last_name', 'value'),
    ]
)
def deactivatesignup(username, password, passwordconf, first_name, last_name):
    # Enable button if all required fields are filled
    enablebtn = all([username, password, passwordconf, first_name, last_name])
    return [not enablebtn]

# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('username_exists_alert', 'is_open'),
        Output('password_mismatch_alert', 'is_open'),
        Output('signup_modal', 'is_open')
    ],
    [
        Input('signup_signupbtn', 'n_clicks')
    ],
    [
        State('first_name', 'value'),
        State('middle_initial', 'value'),
        State('last_name', 'value'),
        State('signup_username', 'value'),
        State('signup_password', 'value'),
        State('signup_passwordconf', 'value')
    ]
)
def saveuser(signup_signupbtn, first_name, middle_initial, last_name, username, password, passwordconf):
    if not signup_signupbtn:
        raise PreventUpdate

    openalert = openmodal = openusernamealert = openpasswordmismatchalert = False

    if username and password and first_name and last_name:
        if password != passwordconf:
            openpasswordmismatchalert = True
        elif db.username_exists(username):
            openusernamealert = True
        else:
            sql = """INSERT INTO users (first_name, middle_initial, last_name, user_name, user_password, user_role)
                     VALUES (%s, %s, %s, %s, %s, 'User')"""  
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
            values = [first_name, middle_initial, last_name, username, encrypt_string(password)]
            db.modifydatabase(sql, values)
            openmodal = True
    else:
        openalert = True

    return [openalert, openusernamealert, openpasswordmismatchalert, openmodal]
