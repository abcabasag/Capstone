from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
from urllib.parse import urlparse, parse_qs

from apps.dbconnect import get_latest_request_class_id, get_latest_request_number, get_latest_email

import os

EMAIL_ADDRESS = os.getenv('scmilay@up.edu.ph')
EMAIL_PASSWORD = os.getenv('brqd mkap mndt zibx')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_address, subject, body):
    EMAIL_ADDRESS = "scmilay@up.edu.ph"
    EMAIL_PASSWORD = "brqd mkap mndt zibx"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

latest_request_number = get_latest_request_number()
latest_email = get_latest_email()

modal_message = f'Your Procurement Request has been successfully submitted.<br><br><div style="font-size: 40px; font-weight: bold;">{latest_request_number}</div><br>is your Request Number for tracking purposes.'

layout = html.Div(
    [
        dbc.Button(html.Img(src='/assets/back.svg'),
                   id='back_button',
                   href='/functions/firstpage_p',  # Adjust this URL to match your home page URL
                   outline=True,
                   color="light"
                   ),
        html.H3('Procurement Request'),
        html.Hr(),
        dbc.Alert(id='PR_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Item", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='PR_item',
                                placeholder='Enter item',
                            ),
                            width=4
                        ),
                        dbc.Col(width=1),
                        dbc.Label("Image", width=1),
                        dbc.Col(
                            html.Div([
                                html.A(
                                    'Click here to upload an image',
                                    href='https://drive.google.com/drive/folders/1kN8-KtJGSB8fu4rISEjap68HfI1AMsdl?usp=sharing',
                                    target="_blank"  # Added target="_blank" to open link in a new tab
                                ),
                                html.Br(), 
                                html.Span("Please make sure that the filename follows the format: [LastName_Item]. For example: delaCruz_Paper"),
                            ]),
                            width=4,
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
                dbc.Row(
                    [
                        dbc.Label("Quantity", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='PR_quantity',
                                placeholder='Enter quantity',
                            ),
                            width=4
                        ),
                    ],
                    className='mb-3 align-items-center'
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Label("Remarks / Specifications", width=2),
                        dbc.Col(
                            dcc.Textarea(
                                id='PR_remarks',
                                placeholder='Remarks',
                                style={'width': '100%'}
                            ),
                            width=10,
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
            dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                'Submit',
                                id='PR_submit',
                                n_clicks=0
                            ),
                            width={"size": 2, "offset": 5}
                        )
                    ]
                )
            ]
        ),
        dcc.Loading(
            id="loading-p",
            type="default",
            children=html.Div(id="loading-output-p", style={"display": "none"})  # Hidden div to trigger loading
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Submission Successful", style={"color": "#0056b3"}),  # Modal header with blue color
                dbc.ModalBody(id='PR_successmodal_body', style={"text-align": "center"}),  # Centered modal body
                dbc.ModalFooter(
                    dbc.Button("Finish", href='/procurement_list', color="primary")  # Blue button
                )
            ],
            centered=True,
            id='PR_successmodal',
            backdrop='static'
        )
    ],
    style={"maxWidth": "1600px", "margin-left": "220px"}
)
    
@app.callback(
    [
        Output('PR_alert', 'color'),
        Output('PR_alert', 'children'),
        Output('PR_alert', 'is_open'),
        Output('PR_successmodal', 'is_open'),
        Output('PR_successmodal', 'children'),
        Output("loading-output-p", "style")
    ],
    [
        Input('PR_submit', 'n_clicks')
    ],
    [
        State('PR_item', 'value'),
        State('PR_quantity', 'value'),
        State('PR_remarks', 'value'),
    ],
)

def PR_saveprofile(submitbtn,
                    PR_item, 
                    PR_quantity, 
                    PR_remarks):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'PR_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            modal_body_content = None

            loading_style = {"display": "block"}

            # Get the latest request_class_id
            request_class_id = db.get_latest_request_class_id()
            latest_email = db.get_latest_email()

            if not PR_item:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please input the item.'
            elif not PR_quantity:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please input the quantity.'
            elif not PR_remarks:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please input the specifications or remarks.'
            else: 

                sql = '''
                    INSERT INTO procurement_request (
                        item, 
                        quantity, 
                        additional_remarks_procu, 
                        procurement_request_delete,
                        Request_Class_ID
                    )
                    VALUES (%s, %s, %s, FALSE, %s)
                '''
                values = [PR_item, PR_quantity, PR_remarks, request_class_id]
                db.modifydatabase(sql, values)

                status_change_sql = '''
                    INSERT INTO Status_Change (
                        Current_Status,
                        Date_updated,
                        Remarks_statchange,
                        Request_Class_ID,
                        Status_ID,
                        user_id,
                        current_ind,
                        delete_ind,
                        inserted_on
                    )
                    VALUES ('Pending', CURRENT_DATE, 'Request received and pending', %s, (SELECT Status_ID FROM Status WHERE Status_Name = 'Pending'), NULL, TRUE, FALSE, CURRENT_TIMESTAMP)
                '''
                
                status_change_values = [
                    request_class_id
                ]

                db.modifydatabase(status_change_sql, status_change_values)

                # If this is successful, we want the successmodal to show
                modal_open = True

                # Fetch the latest request number after submission
                latest_request_number = get_latest_request_number()
                latest_email = get_latest_email()

                to_address_requestor = latest_email
                subject_requestor = "New Procurement Request"
                body_requestor = f"Your Procurement Request has been submitted. You can check its progress in the Check Request Status Tab using your Request Number.\n\nRequest Number: {latest_request_number}\nItem/s: {PR_item}\nQuantity: {PR_quantity}\nRemarks: {PR_remarks}"
                send_email(to_address_requestor, subject_requestor, body_requestor)

                # Send email notification with the label
                to_address_ncts = "genesiscabasag@gmail.com"
                subject_ncts = "New Procurement Request"
                body_ncts = f"A new Procurement Request has been submitted.\n\nRequest Number: {latest_request_number}\nItem/s: {PR_item}\nQuantity: {PR_quantity}\nRemarks: {PR_remarks}"
                send_email(to_address_ncts, subject_ncts, body_ncts)

                # Prepare the modal body content with the updated request number
                modal_body_content = dbc.ModalBody(
                    html.Div(
                        [
                            dbc.ModalHeader(
                            html.H4('Submission Successful', style={"color": "#0056b3"})  # Modal header with blue color
                        ),
                            html.Div('Your Procurement Request has been successfully submitted.', style={'text-align': 'center'}),
                            html.Br(),
                            html.Div(latest_request_number, style={'text-align': 'center', 'font-size': '40px', 'font-weight': 'bold'}),
                            html.Br(),
                            html.Div('is your Request Number for tracking purposes.', style={'text-align': 'center'}),
                            dbc.ModalFooter(
                            dbc.Button(
                                "Finish",
                                href='/user',
                                color="primary"  # Blue button
                            )
                        )
                        ]
                    )
                )

            loading_style = {"display": "none"}
            return [alert_color, alert_text, alert_open, modal_open, modal_body_content, loading_style]

        else: # Callback was not triggered by desired triggers
            raise PreventUpdate
    else:
         raise PreventUpdate
