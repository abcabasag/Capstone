import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime, timedelta

from app import app
from apps import dbconnect as db

from apps.dbconnect import get_latest_request_class_id, get_latest_request_number, get_latest_email

import os

ITALIC_TEXT_STYLE = {
    'font-style': 'italic',
}

time_options = [{"label": f"{hour % 12 if hour % 12 else 12:02d}:{minute:02d} {'AM' if hour < 12 else 'PM'}", 
                 "value": f"{hour % 12 if hour % 12 else 12:02d}:{minute:02d} {'AM' if hour < 12 else 'PM'}"} 
                for hour in range(24) for minute in [0]]

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

modal_message = f'Your Vehicle Dispatch Request has been successfully submitted.<br><br><div style="font-size: 40px; font-weight: bold;">{latest_request_number}</div><br>is your Request Number for tracking purposes.'

# Import necessary libraries
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Style for italic text
ITALIC_TEXT_STYLE = {"fontStyle": "italic"}

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
        dbc.Alert(id='VDR_alert', is_open=False),  # For feedback purposes
        dbc.Form(
            [
                html.H4('Trip Details', style={"color": "#0056b3"}),  # Label for section
                dbc.Row(
                    [
                        dbc.Label("Vehicle", width=1, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dcc.Dropdown(
                                id='VDR_vehicle',
                                placeholder='Vehicle type',
                                style={"border": "1px solid #0056b3"}  # Blue border for dropdown
                            ),
                            width=4
                        ),
                        dbc.Label("Driver", width=1, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='VDR_driver',
                                placeholder='Driver Name',
                                style={"border": "1px solid #0056b3"}  # Blue border for input
                            ),
                            width=4,
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
                dbc.Row(
                    [
                        dbc.Label("Passenger/s", width=1, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='VDR_passenger',
                                placeholder="Passenger/s (Please Specify)",
                                style={"border": "1px solid #0056b3"}  # Blue border for input
                            ),
                            width=4,
                        ),
                    ],
                    className='mb-3 align-items-center'
                ),
                dbc.Row(
                    [
                        dbc.Label("Purpose", width=1, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dcc.Dropdown(
                                id='VDR_purpose',
                                placeholder='Purpose',
                                style={"border": "1px solid #0056b3"}  # Blue border for dropdown
                            ),
                            width=4
                        ),
                        dbc.Label("Purpose Details", width=1, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dbc.Textarea(
                                id='VDR_purpose_others',
                                placeholder='Please input purpose specifications',
                                style={'width': '100%', "border": "1px solid #0056b3"}  # Blue border for textarea
                            ),
                            width=6,
                        ),
                    ],
                    className='mb-3 align-items-center'
                ),
                # Add this inside the dbc.Form where other form elements are defined
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Checkbox(
                                id='terms',
                                label="I agree that the fuel expense and other incidental costs will be shouldered by the requesting party.",
                                value=False,  # Default to not checked
                                style={"display": "none"}  # Initially hidden
                            ),
                            width=8,
                        ),
                    ],
                    className='mb-3 align-items-center'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.P("NCTS vehicles are for the Center's official use only. Trips other than those which are considered official will be subjected to existing NCTS terms and condition on vehicle rental. By filling up this form, you agree with this term and condition."),
                            style=ITALIC_TEXT_STYLE, width=15,
                        ),
                    ],
                    className='mb-3'
                ),
                html.Hr(),  # Line to divide sections
                html.H4('Schedule', style={"color": "#0056b3"}),  # Label for section
                dbc.Row(
                    [
                        dbc.Label("Destination", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='VDR_destination',
                                placeholder='Destination',
                                style={"border": "1px solid #0056b3"}  # Blue border for input
                            ),
                            width=4,
                        ),
                    ],
                    className='mb-3 align-items-center'
                ),
                dbc.Row(
                    [
                        dbc.Label("Departure Date", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='VDR_departure_date',
                                placeholder='Departure Date',
                                month_format='MMM Do, YY',
                                display_format='MMM Do, YY',
                                style={"border": "1px solid #0056b3"}  # Blue border for date picker
                            ),
                            width=4,
                        ),
                        dbc.Label("Departure Time", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dcc.Dropdown(
                                id='VDR_departure_time',
                                options=time_options,
                                placeholder='Time',
                                style={"border": "1px solid #0056b3"}  # Blue border for dropdown
                            ),
                            width=2,
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
                dbc.Row(
                    [
                        dbc.Label("Length of Trip", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='VDR_trip_length_days',
                                placeholder='Number of Days',
                                style={"border": "1px solid #0056b3"}  # Blue border for input
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='VDR_trip_length_hours',
                                placeholder='Number of Hours',
                                style={"border": "1px solid #0056b3"}  # Blue border for input
                            ),
                            width=2,
                        ),
                    ],
                    className='mb-3 align-items-center'
                ),

                dbc.Row(
                    [
                        dbc.Label("Arrival Date", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            html.Div(id='VDR_arrival_date', style={"border": "1px solid #0056b3"}),  # Blue border for div
                            width=2,
                        ),
                        dbc.Col(width=2),
                        dbc.Label("Arrival Time", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            html.Div(id='VDR_arrival_time', style={"border": "1px solid #0056b3"}),  # Blue border for div
                            width=2,
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
                dbc.Row(
                    [
                        dbc.Label("Mode of Borrowing", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dcc.Dropdown(
                                options=[
                                    {"label": "Drop-off", "value": "dropoff"},
                                    {"label": "Pick-up", "value": "pickup"},
                                    {"label": "Wait", "value": "wait"}
                                ],
                                id='VDR_drop_pick',
                                placeholder='Select an option',
                                style={"border": "1px solid #0056b3"}  # Blue border for dropdown
                            ),
                            width=3
                        ),
                        dbc.Col(width=1),
                        dbc.Label("Time", width=1, id='VDR_pickup_time_label', style={'display': 'none', "color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dcc.Dropdown(
                                id='VDR_pickup_time',
                                options=time_options,
                                placeholder='Pickup Time',
                                style={'display': 'none', "border": "1px solid #0056b3"}  # Blue border for dropdown
                            ),
                            width=2,
                            id='VDR_pickup_time_col'
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Label("Remarks", width=2, style={"color": "#0056b3"}),  # Label with blue color
                        dbc.Col(
                            dcc.Textarea(
                                id='VDR_remarks',
                                placeholder='Remarks',
                                style={'width': '100%', "border": "1px solid #0056b3"}  # Blue border for textarea
                            ),
                            width=3,
                        )
                    ],
                    className='mb-3 align-items-center'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                'Submit',
                                id='VDR_submit',
                                n_clicks=0,
                                color="primary",  # Blue button
                                style={"width": "100%"}  # Make the button full width
                            ),
                            width={"size": 2, "offset": 5}
                        )
                    ]
                )
            ]
        ),
        dcc.Loading(
            id="loading-vdr",
            type="default",
            children=html.Div(id="loading-output-vdr", style={"display": "none"})  # Hidden div to trigger loading
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Submission Successful", style={"color": "#0056b3"}),  # Modal header with blue color
                dbc.ModalBody(id='VDR_successmodal_body'),  # Update this line to include an id for dynamic content insertion
                dbc.ModalFooter(
                    dbc.Button("Finish", href='/home', color="primary")  # Blue button
                )
            ],
            centered=True,
            id='VDR_successmodal',
            backdrop='static'
        )
    ],
    style={"maxWidth": "1600px", "margin-left": "220px"}
)

@app.callback(
    Output('VDR_arrival_date', 'children'),
    Output('VDR_arrival_time', 'children'),
    Input('VDR_departure_date', 'date'),
    Input('VDR_departure_time', 'value'),
    Input('VDR_trip_length_days', 'value'),
    Input('VDR_trip_length_hours', 'value')
)
def calculate_arrival_datetime(departure_date, departure_time, trip_length_days, trip_length_hours):
    if departure_date and departure_time and (trip_length_days or trip_length_hours):
        # Convert departure time to datetime object
        departure_datetime = datetime.strptime(departure_date + ' ' + departure_time, '%Y-%m-%d %I:%M %p')

        # Calculate arrival datetime based on departure datetime and trip length
        total_hours = 0
        if trip_length_days:
            total_hours += int(trip_length_days) * 24
        if trip_length_hours:
            total_hours += float(trip_length_hours)

        # Calculate the number of days and hours
        days = total_hours // 24
        remaining_hours = total_hours % 24

        # Calculate the arrival datetime
        arrival_datetime = departure_datetime + timedelta(days=days, hours=remaining_hours)

        # Format arrival date and time
        arrival_date = arrival_datetime.strftime('%b %d, %Y')
        arrival_time = arrival_datetime.strftime('%I:%M %p')

        return arrival_date, arrival_time
    else:
        return '', ''

@app.callback(
    [
        Output('VDR_pickup_time', 'style'),
        Output('VDR_pickup_time_label', 'style'),
        Output('VDR_pickup_time_col', 'width'),
        Output('VDR_pickup_time', 'value')  # Add output for setting value
    ],
    [Input('VDR_drop_pick', 'value')],
    [State('VDR_departure_time', 'value')]  # Add state for departure time
)
def display_time_input(drop_pick_value, departure_time):
    if drop_pick_value == 'pickup':
        # Set pickup time style to block
        pickup_time_style = {'display': 'block'}
        pickup_time_label_style = {'display': 'block'}
        pickup_time_col_width = 2
        
        pickup_time_value = None
    else:
        # Set pickup time style to none
        pickup_time_style = {'display': 'none'}
        pickup_time_label_style = {'display': 'none'}
        pickup_time_col_width = 1
        pickup_time_value = None

    return pickup_time_style, pickup_time_label_style, pickup_time_col_width, pickup_time_value

@app.callback(
    [
        Output('VDR_vehicle', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def VDR_populatevehicle(pathname):
    if pathname == '/functions/vehicledispatchrequest':
        sql = """
        SELECT vehicle_type as label, vehicle_id as value
        FROM vehicle 
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        VDR_vehicle_options = df.to_dict('records')
        return [VDR_vehicle_options]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('VDR_purpose', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def VDR_populatepurpose(pathname):
    if pathname == '/functions/vehicledispatchrequest':
        sql = """SELECT purpose_type as label, purpose_id as value
        FROM purpose 
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        VDR_purpose_options = df.to_dict('records')
        return [VDR_purpose_options]
    else:
        raise PreventUpdate
    
@app.callback(
    Output('terms', 'style'),
    [Input('VDR_purpose', 'value')]
)
def toggle_terms_checkbox(purpose):
    if purpose in [2, 3]:  # 'project' is 2, 'others' is 3
        return {"display": "block"}  # Show the checkbox
    else:
        return {"display": "none"}  # Hide the checkbox

@app.callback(
    [
        Output('VDR_alert', 'color'),
        Output('VDR_alert', 'children'),
        Output('VDR_alert', 'is_open'),
        Output('VDR_successmodal', 'is_open'),
        Output('VDR_successmodal', 'children'),
        Output("loading-output-vdr", "style")
    ],
    [

        Input('VDR_submit', 'n_clicks')
    ],
    [
        State('VDR_vehicle', 'value'),
        State('VDR_driver', 'value'),
        State('VDR_purpose', 'value'),
        State('VDR_passenger', 'value'),
        State('VDR_destination', 'value'),
        State('VDR_departure_date', 'date'),
        State('VDR_departure_time', 'value'),
        State('VDR_trip_length_days', 'value'),
        State('VDR_trip_length_hours', 'value'),
        State('VDR_arrival_date', 'children'),
        State('VDR_arrival_time', 'children'),
        State('VDR_drop_pick', 'value'),
        State('VDR_pickup_time', 'value'),
        State('VDR_remarks', 'value'),
        State('VDR_purpose_others', 'value'),
        State('terms', 'value'),
        State('VDR_vehicle', 'options'),
        State('VDR_purpose', 'options')
    ]
)

def VDR_saveprofile(submitbtn,
                    VDR_vehicle, 
                    VDR_driver, 
                    VDR_purpose, 
                    VDR_passenger, 
                    VDR_destination, 
                    VDR_departure_date, 
                    VDR_departure_time,  
                    VDR_trip_length_days,
                    VDR_trip_length_hours,
                    VDR_arrival_date,
                    VDR_arrival_time, 
                    VDR_drop_pick,
                    VDR_pickup_time,
                    VDR_remarks,
                    VDR_purpose_others,
                    terms,
                    VDR_vehicle_options,
                    VDR_purpose_options):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'VDR_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            modal_body_content = None

            loading_style = {"display": "block"}

            # Get the latest request_class_id
            request_class_id = db.get_latest_request_class_id()
            latest_email = db.get_latest_email()

            if not VDR_vehicle: 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select the vehicle to be borrowed.'
            elif not VDR_purpose:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select the purpose of request.'
            elif not VDR_purpose_others:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please specify purpose details.'
            elif not VDR_passenger:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please input name/s of passenger/s.'
            elif not VDR_destination:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please input the destination.'
            elif not VDR_departure_date:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please input the date of departure.'    
            elif not VDR_departure_time:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please input the time of departure.'      
            elif not (VDR_trip_length_days or VDR_trip_length_hours):
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please input how long is the trip.'
            elif not VDR_drop_pick:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please select mode of claiming the vehicle.'
            elif VDR_drop_pick == 'pickup' and not VDR_pickup_time:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please input the time of pickup.'
            elif not VDR_remarks:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please check remarks.'
            elif VDR_purpose in [2, 3] and not terms:  # Check if purpose is 'project' (2) or 'others' (3)
                alert_open = True
                alert_color = 'danger'
                alert_text = 'You must agree to the terms and conditions to proceed.'
            else:
                # Calculate trip length in days and hours
                trip_length_days = int(VDR_trip_length_days) if VDR_trip_length_days else 0
                trip_length_hours = int(VDR_trip_length_hours) if VDR_trip_length_hours else 0

                # Convert trip length to a combined string value
                trip_length_combined = f"{trip_length_days}_days, {trip_length_hours}_hrs"

                sql = '''
                    INSERT INTO Vehicle_Dispatch_Request (
                        Passengers,
                        Driver_name,
                        Destination,
                        Borrow_time_from,
                        Borrow_time_to,
                        Borrow_date_from,
                        Borrow_date_to,
                        length_of_trip,
                        mode_of_claiming,
                        pickup_time,
                        Remarks_vehicledisp,
                        Vehicle_ID,
                        Purpose_ID,
                        Vehicle_Dispatch_Request_Delete,
                        Request_Class_ID,
                        Purpose_others,
                        terms
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE, %s, %s, %s)
                '''
                values = [
                    VDR_passenger,
                    VDR_driver,
                    VDR_destination,
                    VDR_departure_time,
                    VDR_arrival_time,
                    VDR_departure_date,
                    VDR_arrival_date,
                    trip_length_combined,
                    VDR_drop_pick,
                    VDR_pickup_time, 
                    VDR_remarks,
                    VDR_vehicle,        # Assuming VDR_vehicle is the Vehicle_ID
                    VDR_purpose,        # Assuming VDR_purpose is the Purpose_ID
                    request_class_id,
                    VDR_purpose_others,
                    terms,
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

                modal_open = True

                # Fetch the latest request number after submission
                latest_request_number = get_latest_request_number()
                latest_email = get_latest_email()

                # Fetch requestor's name from request_class table based on email
                requestor_name = db.get_requestor_name_by_email(request_class_id)

                selected_label_vehicle = None
                for option in VDR_vehicle_options:
                    if option['value'] == VDR_vehicle:
                        selected_label_vehicle = option['label']
                        break

                selected_label_purpose = None
                for option in VDR_purpose_options:
                    if option['value'] == VDR_purpose:
                        selected_label_purpose = option['label']
                        break

                to_address_requestor = latest_email
                subject_requestor = "New Vehicle Dispatch Request"
                body_requestor = f"Your Vehicle Dispatch Request has been submitted. You can check its progress in the Check Request Status Tab using your Request Number.\n\nRequest Number: {latest_request_number}\nRequestor: {requestor_name}\nVehicle Type: {selected_label_vehicle}\nPurpose: {selected_label_purpose}\nPurpose Details: {VDR_purpose_others}\nPassenger/s: {VDR_passenger}\nDestination: {VDR_destination}\nDeparture Date: {VDR_departure_date}\nDeparture Time: {VDR_departure_time}\nLength of Trip: {trip_length_combined}\nMode of Borrowing: {VDR_drop_pick}\nRemarks: {VDR_remarks}"
                send_email(to_address_requestor, subject_requestor, body_requestor)

                # Send email notification with the label
                to_address_ncts = "genesiscabasag@gmail.com"
                subject_ncts = "New Vehicle Dispatch Request"
                body_ncts = f"A new Vehicle Dispatch Request has been submitted.\n\nRequest Number: {latest_request_number}\nRequestor: {requestor_name}\nVehicle Type: {selected_label_vehicle}\nPurpose: {selected_label_purpose}\nPurpose Details: {VDR_purpose_others}\nPassenger/s: {VDR_passenger}\nDestination: {VDR_destination}\nDeparture Date: {VDR_departure_date}\nDeparture Time: {VDR_departure_time}\nLength of Trip: {trip_length_combined}\nMode of Borrowing: {VDR_drop_pick}\nRemarks: {VDR_remarks}"
                send_email(to_address_ncts, subject_ncts, body_ncts)

                # Prepare the modal body content with the updated request number
                modal_body_content = dbc.ModalBody(
                    html.Div(
                        [
                            dbc.ModalHeader(
                            html.H4('Submission Successful', style={"color": "#0056b3"})  # Modal header with blue color
                        ),
                            html.Div('Your Vehicle Dispatch Request has been successfully submitted.', style={'text-align': 'center'}),
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
                        ]
                    )
                )

            loading_style = {"display": "none"}
            return [alert_color, alert_text, alert_open, modal_open, modal_body_content, loading_style]
        else: 
            raise PreventUpdate
    else:
        raise PreventUpdate
