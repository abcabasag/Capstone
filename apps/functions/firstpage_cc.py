from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
from urllib.parse import urlparse, parse_qs

# Define a common style for input fields
input_style = {
    "border": "1px solid #0056b3",
    "border-radius": "4px",
    "width": "100%",
    "height": "38px"  # Ensures all input fields have the same height
}

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
        html.H2('Citizens Charter Request', style={"color": "#0056b3", "text-align": "left"}),  # Page Header with blue color and left alignment
        html.Hr(),
        dbc.Alert(id='ccfp_alert', is_open=False),  # For feedback purposes
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
                                id='ccfirst_name',
                                placeholder='First Name',
                                style=input_style  # Blue border, rounded corners, and uniform height for input
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='ccmiddle_initial',
                                placeholder='M.I.',
                                style=input_style  # Blue border, rounded corners, and uniform height for input
                            ),
                            width=1,
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='cclast_name',
                                placeholder='Last Name',
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
                            dbc.Label("Group / Office", style={"color": "#0056b3"}), width=2  # Label with blue color
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='ccunit_organization',
                                placeholder='Input Group / Office',
                                style=input_style  # Blue border, rounded corners, and uniform height for input
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
                                id='cc_email',
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
                                id='cc_number',
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
                                id='ccfp_submit',
                                href="/functions/add_cc",
                                n_clicks=0,
                                disabled=True,  # Initially disable the button
                                color="primary",  # Blue button
                                style={"width": "100%"}  # Make the button full width
                            ),
                            width={"size": 2, "offset": 5}
                        )
                    ]
                ),
                dbc.Row(
                    dbc.Col(
                            dbc.Label("Click the button only once.", style={"color": "#0056b3", "text-align": "center"}), width=2  # Label with blue color
                        ),
                ),
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Submission Successful", style={"color": "#0056b3"}),  # Modal header with blue color
                dbc.ModalBody(id='ccfp_successmodal_body', style={"text-align": "center"}),  # Centered modal body
                dbc.ModalFooter(
                    dbc.Button("Finish", href='/home', color="primary")  # Blue button
                )
            ],
            centered=True,
            id='ccfp_successmodal',
            backdrop='static'
        )
    ],
    style={"maxWidth": "1600px", "margin-left": "220px"}
)

# Callback to enable/disable the submit button based on form completeness
@app.callback(
    Output('ccfp_submit', 'disabled'),
    [
        Input('ccfirst_name', 'value'),
        Input('cclast_name', 'value'),
        Input('ccunit_organization', 'value'),
        Input('cc_email', 'value'),
        Input('cc_number', 'value'),
    ]
)
def cctoggle_submit_button(ccfirst_name, cclast_name, ccunit_organization, cc_email, cc_number):
    if all([ccfirst_name, cclast_name, ccunit_organization, cc_email, cc_number]):
        return False
    return True


@app.callback(
    [
        Output('ccfp_alert', 'color'),
        Output('ccfp_alert', 'children'),
        Output('ccfp_alert', 'is_open')
    ],
    [
        Input('ccfp_submit', 'n_clicks')
    ],
    [
        State('ccfirst_name', 'value'),
        State('ccmiddle_initial', 'value'),
        State('cclast_name', 'value'),
        State('ccunit_organization', 'value'),
        State('cc_email', 'value'),
        State('cc_number', 'value'),
    ]
)

def ccfp_saveprofile(submitbtn,
                   ccfirst_name,
                   ccmiddle_initial,
                   cclast_name,
                   ccunit_organization,
                   cc_email,
                   cc_number):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'ccfp_submit' or not submitbtn:
        raise PreventUpdate

    alert_open = False
    alert_color = ''
    alert_text = ''

    if not all([ccfirst_name, cclast_name, ccunit_organization, cc_email, cc_number]):
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please supply all required information.'
    else:
        try:
            sql = '''
                INSERT INTO request_class (rc_first_name, rc_middle_i, rc_last_name, organization, email, contact_number, request_class_delete)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            values = [ccfirst_name, ccmiddle_initial, cclast_name, ccunit_organization, cc_email, cc_number, False]
            db.modifydatabase(sql, values)
        except Exception as e:
            alert_open = True
            alert_color = 'danger'
            alert_text = f"An error occurred: {str(e)}"

    return alert_color, alert_text, alert_open
