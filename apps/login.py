import hashlib

import dash_bootstrap_components as dbc
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Please input your login credentials', style={"color": "#0056b3"}),  # Updated color
        html.Hr(),
        dbc.Alert('Username or password is incorrect.', color="danger", id='login_alert', is_open=False),
        dbc.Row(
            [
                dbc.Label("Username", width=2, style={"color": "#0056b3"}),  # Updated color
                dbc.Col(
                    dbc.Input(
                        type="text", id="login_username", placeholder="Enter username",
                        style={"border": "1px solid #0056b3"}  # Added border style
                    ),
                    width=6,
                ),
            ],
            className="mb-3 align-items-center",  # Added align-items-center for consistent alignment
        ),
        dbc.Row(
            [
                dbc.Label("Password", width=2, style={"color": "#0056b3"}),  # Updated color
                dbc.Col(
                    dbc.Input(
                        type="password", id="login_password", placeholder="Enter password",
                        style={"border": "1px solid #0056b3"}  # Added border style
                    ),
                    width=6,
                ),
            ],
            className="mb-3 align-items-center",  # Added align-items-center for consistent alignment
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button('Login', color="primary", id='login_loginbtn', style={"width": "100%"}),  # Updated color
                    width={"size": 2, "offset": 5}
                )
            ],
            className="mb-3 align-items-center",  # Added align-items-center for consistent alignment
        ),
    ],
    style={'max-width': '1600px', 'margin-left': '220px'},  # Updated max-width
)

@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
        Output('currentrole', 'data'),  # Output for storing current role
    ],
    [
        Input('login_loginbtn', 'n_clicks'), # begin login query via button click
        Input('sessionlogout', 'modified_timestamp'), # reset session userid to -1 if logged out
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),   
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'), 
        State('url', 'pathname'), 
    ]
)
def loginprocess(loginbtn, sessionlogout_time, username, password, sessionlogout, currentuserid, pathname):
    
    ctx = callback_context
    
    if ctx.triggered:
        openalert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    currentrole = -1  # Initialize currentrole before conditional blocks
    
    if eventid == 'login_loginbtn': # trigger for login process
    
        if loginbtn and username and password: # Include user_rolein the query
            sql = """SELECT user_id, user_role      
                     FROM users
                     WHERE 
                         user_name = %s AND
                         user_password = %s AND
                         NOT user_delete_ind"""
            
            # we match the encrypted input to the encrypted password in the db
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
            
            values = [username, encrypt_string(password)]
            cols = ['userid', 'role']  # Retrieve user_role from the query result
            df = db.querydatafromdatabase(sql, values, cols)
            
            if df.shape[0]: # if query returns rows
                currentuserid = df['userid'][0]
                currentrole = df['role'][0]  # Store the user's role
            else:
                currentuserid = -1
                openalert = True
                
    elif eventid == 'sessionlogout' and pathname == '/logout': # reset the userid if logged out
        currentuserid = -1
        currentrole = -1  # Reset role upon logout
        
    else:
        raise PreventUpdate
    
    return [openalert, currentuserid, currentrole]

@app.callback(
    Output('url', 'pathname'),
    [Input('currentuserid', 'modified_timestamp')],
    [State('currentuserid', 'data'),
     State('url', 'pathname')]
)
def routelogin(logintime, userid, current_path):
    ctx = callback_context
    if ctx.triggered:
        if '/logout' in current_path:
            return '/'  # Redirect to home page upon logout
        elif userid > 0:
            return '/user'  # Redirect logged-in users to procurement page
    raise PreventUpdate
