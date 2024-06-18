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
            href='/procurement_list',  # Adjust this URL to match your home page URL
            outline=True,
            color="light",
            style={"margin-bottom": "10px"}  # Add some space below the button
        ),
        html.H2('Procurement Request', style={"color": "#0056b3", "text-align": "left"}),  # Page Header with blue color and left alignment
        html.Hr(),
        dbc.Alert(id='pfp_alert', is_open=False),  # For feedback purposes
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
                                id='pfirst_name',
                                placeholder='First Name',
                                style=input_style  # Blue border, rounded corners, and uniform height for input
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='pmiddle_initial',
                                placeholder='M.I.',
                                style=input_style  # Blue border, rounded corners, and uniform height for input
                            ),
                            width=1,
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='plast_name',
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
                                id='punit_organization',
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
                                id='p_email',
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
                                id='p_number',
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
                                dbc.Label("Date Needed", style={"color": "#0056b3"}), width=2  # Label with blue color
                        ),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='p_date_needed',
                                placeholder='Date Needed',
                                month_format='MMM Do, YY',
                            ),
                            width=4
                        ),   
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                'Next',
                                id='pfp_submit',
                                href="/functions/procurement",
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
                        [
                            html.Label("Click the 'Next' button "),
                            html.Span(" ONCE", style={"font-weight": "bold"}),
                            html.Label("."),
                        ],
                        width={"size": 2, "offset": 5}  # Centering the column with offset
                    ),
                ),                
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Submission Successful", style={"color": "#0056b3"}),  # Modal header with blue color
                dbc.ModalBody(id='pfp_successmodal_body', style={"text-align": "center"}),  # Centered modal body
                dbc.ModalFooter(
                    dbc.Button("Finish", href='/home', color="primary")  # Blue button
                )
            ],
            centered=True,
            id='pfp_successmodal',
            backdrop='static'
        )
    ],
    style={"maxWidth": "1600px", "margin-left": "220px"}
)

# Callback to enable/disable the submit button based on form completeness
@app.callback(
    Output('pfp_submit', 'disabled'),
    [
        Input('pfirst_name', 'value'),
        Input('plast_name', 'value'),
        Input('punit_organization', 'value'),
        Input('p_email', 'value'),
        Input('p_number', 'value'),
        Input('p_date_needed', 'date')
    ]
)
def ptoggle_submit_button(pfirst_name, plast_name, punit_organization, p_email, p_number,p_date_needed):
    if all([pfirst_name, plast_name, punit_organization, p_email, p_number, p_date_needed]):
        return False
    return True


@app.callback(
    [
        Output('pfp_alert', 'color'),
        Output('pfp_alert', 'children'),
        Output('pfp_alert', 'is_open')
    ],
    [
        Input('pfp_submit', 'n_clicks')
    ],
    [
        State('pfirst_name', 'value'),
        State('pmiddle_initial', 'value'),
        State('plast_name', 'value'),
        State('punit_organization', 'value'),
        State('p_email', 'value'),
        State('p_number', 'value'),
        State('p_date_needed', 'date')
    ]
)

def pfp_saveprofile(submitbtn,
                   pfirst_name,
                   pmiddle_initial,
                   plast_name,
                   punit_organization,
                   p_email,
                   p_number,
                   p_date_needed):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'pfp_submit' or not submitbtn:
        raise PreventUpdate

    alert_open = False
    alert_color = ''
    alert_text = ''

    if not all([pfirst_name, plast_name, punit_organization, p_email, p_number, p_date_needed]):
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please supply all required information.'
    else:
        try:
            sql = '''
                INSERT INTO request_class (rc_first_name, rc_middle_i, rc_last_name, organization, email, contact_number, date_needed)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            values = [pfirst_name, pmiddle_initial, plast_name, punit_organization, p_email, p_number, p_date_needed]
            db.modifydatabase(sql, values)
        except Exception as e:
            alert_open = True
            alert_color = 'danger'
            alert_text = f"An error occurred: {str(e)}"

    return alert_color, alert_text, alert_open
