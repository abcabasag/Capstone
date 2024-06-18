import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime, timedelta
from io import StringIO
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app import app
from apps import dbconnect as db

# Set to track notified request numbers
notified_requests = set()

def calculate_pending_minutes(date_requested):
    # Calculate the difference in minutes between date_requested and now
    minutes_pending = (datetime.now() - date_requested).total_seconds() / 60
    return minutes_pending

EMAIL_ADDRESS = os.getenv('upncts@up.edu.ph')
EMAIL_PASSWORD = os.getenv('mzdg spet exnp qbax')

def send_pending_notification(request_number):
    subject = 'Citizen Charter Request Pending for 3 Minutes'
    body = f"Good day,\n\nRequest {request_number} has been pending for 3 minutes.\n\nPlease take necessary action.\n\nBest regards,\nUP NCTS REQUEST MANAGEMENT SYSTEM"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'janmaeavila@gmail.com'  # Update with recipient's email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

layout = html.Div(
    [
        dbc.Button(
            html.Img(src='/assets/back.svg'),
            id='back_button',
            href='/user',  # Adjust this URL to match your home page URL
            outline=True,
            color="light",
            style={"margin-bottom": "10px"}  # Add some space below the button
        ),
        html.H2('Citizen Charter List'),  # Page Header
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3('Manage Records of Citizen Charter Requests')
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Hr(),
                        html.Div(
                            [
                                html.H4('Find Request'),
                                dbc.Form(
                                    dbc.Row(
                                        [
                                            dbc.Label("Search Request", width=1),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id='cc_requestfilter',
                                                    placeholder='Request Number, Requestor First Name, Requestor Last Name, or Request Type'
                                                ),
                                                width=5
                                            ),
                                            dbc.Label("Filter by Date Requested:", width=2),
                                            dbc.Col(
                                                dcc.DatePickerSingle(
                                                    id='ccdate_from',
                                                    placeholder='Start Date',
                                                    style={'width': '130px', 'font-size': '12px'}
                                                ),
                                                width='auto'
                                            ),
                                            dbc.Label("to", width='auto', style={'text-align': 'center', 'padding-top': '10px'}),
                                            dbc.Col(
                                                dcc.DatePickerSingle(
                                                    id='ccdate_to',
                                                    placeholder='End Date',
                                                    style={'width': '130px', 'font-size': '12px'}
                                                ),
                                                width='auto'
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "X",
                                                    id='ccclear_date_filter',
                                                    color='danger',
                                                    size='sm',
                                                    style={'margin-left': '10px'}
                                                ),
                                                width='auto'
                                            )
                                        ],
                                        className='mb-3 align-items-center'
                                    )
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button("Export CSV", id="ccbtn_csv", color="primary"),
                                            width='auto'
                                        ),
                                        dcc.Download(id="ccdownload-dataframe-csv")
                                    ],
                                    className='mb-3'
                                ),
                                html.Div(id='ccrow_count'),  # Row count display here
                                html.Div(
                                    "Table with citizen charter requests will go here.",
                                    id='cc_requestlist'
                                )
                            ]
                        ),
                        dcc.Interval(
                            id='interval-component',
                            interval=60 * 1000,  # Check every 1 minute (milliseconds)
                            n_intervals=0
                        )
                    ]
                )
            ]
        )
    ],
    style={'max-width': '1500px', 'margin-left': '220px'},
)

@app.callback(
    [
        Output('cc_requestlist', 'children'),
        Output('ccrow_count', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('cc_requestfilter', 'value'),
        Input('ccdate_from', 'date'),  
        Input('ccdate_to', 'date'),
        Input('interval-component', 'n_intervals')
    ]
)
def cchome_loadrequestlist(pathname, searchterm, ccdate_from, ccdate_to, n_intervals):
    if pathname == '/view_cc_list':
        CCcolumns_to_select = [
            "cc_request_id",
            "request_number",
            "rc_first_name",
            "rc_middle_i",
            "rc_last_name",
            "email",
            "contact_number",
            "organization",
            "date_requested",
            "date_started",
            "request_type",
            "group_name",
            "additional_remarks_cc",
            "current_status", 
            "date_updated", 
            "remarks_statchange",
            "r.request_class_id"
        ]

        sql = f"""
            SELECT {', '.join(CCcolumns_to_select)}
            FROM citizen_charter_request m
            INNER JOIN request_class r ON m.request_class_id = r.request_class_id
            INNER JOIN status_change s ON r.request_class_id = s.request_class_id
            INNER JOIN request_type g ON m.request_type_id = g.request_type_id
            INNER JOIN group_citizen_charter h ON g.group_id = h.group_id
            WHERE 1=1
        """
        values = []

        if searchterm:
            search_terms = searchterm.split()
            search_conditions = []

            for term in search_terms:
                sub_conditions = []
                sub_conditions.append("request_number ILIKE %s")
                sub_conditions.append("rc_first_name ILIKE %s")
                sub_conditions.append("rc_last_name ILIKE %s")
                sub_conditions.append("request_type ILIKE %s")
                values.extend([f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"])
                search_conditions.append("(" + " OR ".join(sub_conditions) + ")")

            sql += " AND " + " AND ".join(search_conditions)
        
        if ccdate_from and ccdate_to:
            # Adjust end date by adding one day
            date_to_adjusted = (datetime.strptime(ccdate_to, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            sql += " AND date_requested BETWEEN %s AND %s"
            values.extend([ccdate_from, date_to_adjusted])

        df = db.querydatafromdatabase(sql, values, CCcolumns_to_select)

        if df.shape[0]:  # Check if query returned anything
            # Fix column names
            df.columns = [
                "Citizen Charter ID",
                "Request Number",
                "First Name",
                "Middle Initial",
                "Last Name",
                "Email",
                "Contact Number",
                "Unit/Organization",
                "Date Requested",
                "Date Started",
                "Request Type",
                "Group Assigned",
                "Remarks",
                "Current Status",
                "Date Updated of Status",
                "Remarks on Status",
                "Request Class ID"
            ]

            # Filter for requests pending exactly 3 minutes and send notifications
            if 'Date Requested' in df.columns:
                df['Date Requested'] = pd.to_datetime(df['Date Requested'])  # Ensure 'Date Requested' is datetime type
                df['Pending Minutes'] = df['Date Requested'].apply(calculate_pending_minutes)
                pending_requests = df[(df['Pending Minutes'] >= 3) & (df['Pending Minutes'] <= 3.99)]
                # Iterate over pending requests to send notifications
                for index, row in pending_requests.iterrows():
                    request_number = row['Request Number']

                    if request_number not in notified_requests:
                        send_pending_notification(request_number)
                        notified_requests.add(request_number)

            # Remove 'Pending Minutes' column before displaying the table
            if 'Pending Minutes' in df.columns:
                df.drop(columns=['Pending Minutes'], inplace=True)
                
            buttons = []
            for request_class_id in df['Request Class ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Update Status', href=f'/update_status_request?mode=edit&id={request_class_id}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            df = df.drop(columns=['Request Class ID'])  # Remove the ID column

            table_container_style = {
                'overflow-x': 'auto',
                'max-width': '100%'
            }

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', responsive=True, style=table_container_style)
            row_count = html.Div(f"Total Rows: {df.shape[0]}")
            return [table, row_count]
        else:
            return ["No records to display", "Total Rows: 0"]
    else:
        raise PreventUpdate

@app.callback(
    Output('ccdownload-dataframe-csv', 'data'),
    Input('ccbtn_csv', 'n_clicks'),
    State('cc_requestfilter', 'value'),
    State('ccdate_from', 'date'),
    State('ccdate_to', 'date'),
    prevent_initial_call=True
)
def download_csv(n_clicks, searchterm, ccdate_from, ccdate_to):
    # Define the columns you want to retrieve from the database
    columns_to_select = [
        "cc_request_id",
        "request_number",
        "rc_first_name",
        "rc_middle_i",
        "rc_last_name",
        "email",
        "contact_number",
        "organization",
        "date_requested",
        "date_started",
        "request_type",
        "group_name",
        "additional_remarks_cc",
        "current_status", 
        "date_updated", 
        "remarks_statchange"
    ]

    # Base SQL query
    sql = f"""
        SELECT {', '.join(columns_to_select)}
        FROM citizen_charter_request m
        INNER JOIN request_class r ON m.request_class_id = r.request_class_id
        INNER JOIN status_change s ON r.request_class_id = s.request_class_id
        INNER JOIN request_type g ON m.request_type_id = g.request_type_id
        INNER JOIN group_citizen_charter h ON g.group_id = h.group_id
        WHERE 1=1
    """
    values = []

    # Add search term filter if provided
    if searchterm:
            search_terms = searchterm.split()
            search_conditions = []

            for term in search_terms:
                sub_conditions = []
                sub_conditions.append("request_number ILIKE %s")
                sub_conditions.append("rc_first_name ILIKE %s")
                sub_conditions.append("rc_last_name ILIKE %s")
                sub_conditions.append("request_type ILIKE %s")
                values.extend([f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"])
                search_conditions.append("(" + " OR ".join(sub_conditions) + ")")

            sql += " AND " + " AND ".join(search_conditions)
    
    # Add date range filter if provided
    if ccdate_from and ccdate_to:
        # Adjust end date by adding one day
        date_to_adjusted = (datetime.strptime(ccdate_to, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        sql += " AND date_requested BETWEEN %s AND %s"
        values.extend([ccdate_from, date_to_adjusted])

    # Execute the query
    df = db.querydatafromdatabase(sql, values, columns_to_select)

    if df.shape[0]:  # Check if query returned anything
        # Fix column names
        df.columns = [
            "Citizen Charter ID",
            "Request Number",
            "First Name",
            "Middle Initial",
            "Last Name",
            "Unit/Organization",
            "Email",
            "Contact Number",
            "Date Requested",
            "Date Started",
            "Request Type",
            "Group Assigned",
            "Remarks",
            "Current Status",
            "Date Updated of Status",
            "Remarks on Status"

        ]

        # Use StringIO to save the dataframe to a CSV string
        csv_string = StringIO()
        df.to_csv(csv_string, index=False)
        csv_string.seek(0)
        
        return dict(content=csv_string.getvalue(), filename="citizen_charter_requests.csv")

    raise PreventUpdate

@app.callback(
    Output('ccdate_from', 'date'),
    Output('ccdate_to', 'date'),
    Input('ccclear_date_filter', 'n_clicks'),
    prevent_initial_call=True
)
def ccclear_date_filters(n_clicks):
    # Reset both date inputs to None
    return None, None
