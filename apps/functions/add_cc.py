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

EMAIL_ADDRESS = os.getenv('upncts@up.edu.ph')
EMAIL_PASSWORD = os.getenv('mzdg spet exnp qbax')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_address, subject, body):
    EMAIL_ADDRESS = "upncts@up.edu.ph"
    EMAIL_PASSWORD = "mzdg spet exnp qbax"
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

modal_message = f'Your Citizen Charter Request has been successfully submitted.<br><br><div style="font-size: 40px; font-weight: bold;">{latest_request_number}</div><br>is your Request Number for tracking purposes.'

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
        html.H2('Citizen Charter Request', style={"color": "#0056b3"}),  # Page Header with blue color
        html.Hr(),
        dbc.Alert(id='add_cc_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                html.H4('Request Details', style={"color": "#0056b3"}),  # Label for section
                dbc.Row(
                    [
                        dbc.Label("Citizen Charter Request Type", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dcc.Dropdown(
                                id='ccrequesttype',
                                placeholder='Select Request Type',
                                style={"border": "1px solid #0056b3"}  # Blue border for dropdown
                            ),
                            width=4
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
                # Add a div to display the italic text
                dbc.Row(
                    dbc.Col(
                        html.Div(id='selected_request_type', style={'font-style': 'italic', 'color': '#0056b3'}),
                        width={"size": 6, "offset": 2}
                    ),
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Remarks", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dbc.Textarea(
                                id='add_cc_remarks',
                                placeholder='Please input additional details here.',
                                style={'width': '100%', "border": "1px solid #0056b3"}  # Blue border for textarea
                            ),
                            width=8,
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                'Submit',
                                id='add_cc_submit',
                                n_clicks=0,
                                color="primary",  # Blue button
                                style={"width": "100%"}  # Make the button full width
                            ),
                            width={"size": 2, "offset": 5}
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Click the 'Submit' button "),
                        html.Span(" ONCE", style={"font-weight": "bold"}),
                        html.Label(". Wait for the Request Number to pop up, then click the 'Finish' button."),
                    ],
                    width={"size": 8, "offset": 2},  # Adjusted width for better centering and spacing
                    style={"text-align": "center", "margin-top": "10px"}  # Centering the content and adding margin at the top
                ),
            ]
        ),
        dcc.Loading(
            id="loading-cc",
            type="default",
            children=html.Div(id="loading-output-cc", style={"display": "none"})  # Hidden div to trigger loading
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Submission Successful", style={"color": "#0056b3"}),  # Modal header with blue color
                dbc.ModalBody(id='add_cc_successmodal_body', style={"text-align": "center"}),  # Centered modal body
                dbc.ModalFooter(
                    dbc.Button("Finish", href='/home', color="primary")  # Blue button
                )
            ],
            centered=True,
            id='add_cc_successmodal',
            backdrop='static',
        )
    ],
    style={"maxWidth": "1600px", "margin-left": "220px"}
)

@app.callback(
    [
        Output('ccrequesttype', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def addcc_populateccrequesttype(pathname):
    if pathname == '/functions/add_cc':
        sql = """SELECT request_type as label, request_type_id as value
        FROM request_type
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        requesttype = df.to_dict('records')
        return [requesttype]
    else:
        raise PreventUpdate

@app.callback(
    Output('selected_request_type', 'children'),
    [Input('ccrequesttype', 'value')],
    [State('ccrequesttype', 'options')]
)
def update_selected_request_type(value, options):
    if value is None:
        return ""
    
    messages = {
        1: "This process allows any individual or organization to tap NCTS technical expertise in conducting research, extension and capacity building activities in the fields of transportation planning, traffic engineering, road traffic safety, traffic law enforcement and other transport related studies.",
        2: "The Center provides assistance in academic research to undergraduate and graduate students in the University. This activity includes support in facilitating thesis advisory, thesis authorship and research contributor.",
        3: "The Center provides extension services thru provision of technical expertise. This activity seeks to involve NCTS personnel in formal membership and participation in various Technical Working Group (TWG).",
        4: "This activity facilitates NCTS technical assistance to UP students in available transport software use and tutorship.",
        5: "This activity involves the practical and academic exposure of students in the Center's line of activities.",
        6: "This service involves the facilitation of hosting exchange students, researchers including specific research projects related to transport.",
        7: "The Center conducts several Civil Service Commission (CSC) and Professional Regulation Commission (PRC) Accredited Programs in a year to capacitate any individual involve in the fields of traffic administration, road safety audit, road works safety, traffic law enforcement, emissions inventory and other transport related topics. The process illustrates on how qualified personnel may avail of the service.",
        8: "The Center provides capacity building, training and extension service thru the development and conduct of requested technical-specific training programs. This service is specifically designed to address and capacitate the technical needs of personnel in local government units, government offices and private organization in the field of transportation.",
        9: "The Center conducts free webinars on current and relevant transport related topics. The process illustrates on how qualified personnel may avail of the service.",
        10: "The activity involves the verification and validation of certificates on training programs attended by the participants and lecturers. The issuance of the certified true copies of the said certificates are being accomplished for any legal purpose that may serve them.",
        11: "The National Center for Transportation Studies Data and Information Unit is regularly collecting transport data from different transport related agencies. The data gathered are available for any user upon evaluation and approval of formal request",
        12: "The NCTS Library service includes the granting of access to use NCTS library facility, materials, and resources for UP and non-UP clients. The process below describes on how to avail of the service.",
        13: "The NCTS Library only allows U.P. student, faculty, and employees to borrow materials.",
        14: "The NCTS Library will impose a P2.00 fine for regular books and P50.00 for special collections for each day beyond due date.",
        15: "The NCTS Library is accepting donations to upgrade its library resources and collections. Acceptance of donations involves sending intent letter, confirmation of donations, and issuance of acknowledgement letter.",
        16: "Part of the technical and extension service being provided by the Center includes accommodating request for resource person/s in lectures, seminars, workshops and interviews. The process involved the allocation of NCTS personnel on the scheduled activities.",
        17: "The Center accommodates and renders extension services to UP community's requests for transport related assistances.",
        18: "The Center accommodates request for the use of NCTS equipment and facilities. The process involves the granting of permit to use equipment and facility.",
    }
    
    message = messages.get(value, "You have selected a request type.")
    return message

@app.callback(
    [
        Output('add_cc_alert', 'color'),
        Output('add_cc_alert', 'children'),
        Output('add_cc_alert', 'is_open'),
        Output('add_cc_successmodal', 'is_open'),
        Output('add_cc_successmodal', 'children'),
        Output("loading-output-cc", "style")
    ],
    [
        Input('add_cc_submit', 'n_clicks')
    ],
    [
        State('ccrequesttype', 'value'),
        State('add_cc_remarks', 'value'),
        State('ccrequesttype', 'options')
    ],
)
def VDR_saveprofile(submitbtn,
                    ccrequesttype,
                    add_cc_remarks,
                    ccrequesttype_options):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'add_cc_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            modal_body_content = None

            loading_style = {"display": "block"}

            # Get the latest request_class_id
            request_class_id = db.get_latest_request_class_id()
            latest_email = db.get_latest_email()

            if not ccrequesttype: 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select the request type.'
            elif not add_cc_remarks:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please input remarks.'
            else:
                sql = '''
                    INSERT INTO Citizen_Charter_Request (
                        additional_remarks_cc,
                        request_type_id,
                        citizen_charter_request_Delete,
                        Request_Class_ID
                    )
                    VALUES (%s, %s, FALSE, %s)
                '''
                values = [
                    add_cc_remarks,
                    ccrequesttype,
                    request_class_id
                ]
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

                # If this is successful, we want the success modal to show
                modal_open = True

                # Fetch the latest request number after submission
                latest_request_number = get_latest_request_number()
                latest_email = get_latest_email()

                # Fetch requestor's name from request_class table based on email
                requestor_name_cc = db.get_requestor_name_by_email(request_class_id)

                selected_label_cc = None
                for option in ccrequesttype_options:
                    if option['value'] == ccrequesttype:
                        selected_label_cc = option['label']
                        break

                to_address_requestor = latest_email
                subject_requestor = "New Citizen Charter Request"
                body_requestor = f"Your Citizen Charter Request has been submitted. You can check its progress in the Check Request Status Tab using your Request Number.\n\nRequest Number: {latest_request_number}\nRequestor: {requestor_name_cc}\nRequest Type: {selected_label_cc}\nRemarks: {add_cc_remarks}"
                send_email(to_address_requestor, subject_requestor, body_requestor)

                # Send email notification with the label
                to_address_ncts = "scmilay@up.edu.ph"
                subject_ncts = "New Citizen Charter Request"
                body_ncts = f"A new Citizen Charter Request has been submitted.\n\nRequest Number: {latest_request_number}\nRequestor: {requestor_name_cc}\nRequest Type: {selected_label_cc}\nRemarks: {add_cc_remarks}"
                send_email(to_address_ncts, subject_ncts, body_ncts)

                # Prepare the modal body content with the updated request number
                modal_body_content = dbc.ModalBody(
                html.Div(
                    [
                        dbc.ModalHeader(
                            html.H4('Submission Successful', style={"color": "#0056b3"})  # Modal header with blue color
                        ),
                        html.Div('Your Citizen Charter Request has been successfully submitted.', style={'text-align': 'center'}),
                        html.Br(),
                        html.Div(latest_request_number, style={'text-align': 'center', 'font-size': '40px', 'font-weight': 'bold'}),
                        html.Br(),
                        html.Div('is your Request Number for tracking purposes.', style={'text-align': 'center'}),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Finish",
                                href='/home',
                                color="primary"  # Blue button
                            )
                        )
                    ],
                )
            )
            loading_style = {"display": "none"}  # Hide loading spinner after processing
            return [alert_color, alert_text, alert_open, modal_open, modal_body_content, loading_style]
        else: 
            raise PreventUpdate
    else:
        raise PreventUpdate
