import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime, timedelta
from io import StringIO

# Let us import the app object in case we need to define callbacks here
from app import app
# for DB needs
from apps import dbconnect as db

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
        html.H2('Vehicle Dispatch List'),  # Page Header
        html.Hr(),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    [
                        html.H3('Manage Records of Vehicle Dispatch Requests')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Hr(),
                        html.Div(  # Create section to show list of vehicle dispatch requests
                            [
                                html.H4('Find Request'),
                                dbc.Form(
                                    dbc.Row(
                                        [
                                            dbc.Label("Search Request", width=1),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id='VDR_requestfilter',
                                                    placeholder='Request Number, Requestor First Name, Requestor Last Name, Vehicle Type, or Purpose'
                                                ),
                                                width=5
                                            ),
                                            dbc.Label("Filter by Date Requested:", width=2),
                                            dbc.Col(
                                                dcc.DatePickerSingle(
                                                    id='date_from',
                                                    placeholder='Start Date',
                                                    style={'width': '130px', 'font-size': '12px'}
                                                ),
                                                width='auto'
                                            ),
                                            dbc.Label("to", width='auto', style={'text-align': 'center', 'padding-top': '10px'}),
                                            dbc.Col(
                                                dcc.DatePickerSingle(
                                                    id='date_to',
                                                    placeholder='End Date',
                                                    style={'width': '130px', 'font-size': '12px'}
                                                ),
                                                width='auto'
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "X",
                                                    id='clear_date_filter',
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
                                            dbc.Button("Export CSV", id="btn_csv", color="primary"),
                                            width='auto'
                                        ),
                                        dcc.Download(id="download-dataframe-csv")
                                    ],
                                    className='mb-3'
                                ),
                                html.Div(id='row_count'),  # Row count display here
                                html.Div(
                                    "Table with vehicle dispatch requests will go here.",
                                    id='VDR_requestlist'
                                )
                            ]
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
        Output('VDR_requestlist', 'children'),
        Output('row_count', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('VDR_requestfilter', 'value'),  # changing the text box value should update the table
        Input('date_from', 'date'),  # Start date for the date range filter
        Input('date_to', 'date')  # End date for the date range filter
    ]
)
def VDRhome_loadrequestlist(pathname, searchterm, date_from, date_to):
    if pathname == '/view_request':
        # Define the columns you want to retrieve from the database
        columns_to_select = [
            "vehicle_dispatch_id",
            "request_number",
            "rc_first_name",
            "rc_middle_i",
            "rc_last_name",
            "organization",
            "email",
            "contact_number",
            "date_requested",
            "date_started",
            "vehicle_type",
            "passengers",
            "driver_name",
            "purpose_type",
            "destination",
            "borrow_date_from",
            "borrow_time_from",
            "borrow_date_to",
            "borrow_time_to",
            "length_of_trip",
            "mode_of_claiming",
            "pickup_time",
            "remarks_vehicledisp",
            "current_status", 
            "date_updated", 
            "remarks_statchange",
            "r.request_class_id"
        ]

        # Base SQL query
        sql = f"""
            SELECT {', '.join(columns_to_select)}
            FROM vehicle_dispatch_request v
            INNER JOIN request_class r ON v.request_class_id = r.request_class_id
            INNER JOIN status_change s ON r.request_class_id = s.request_class_id
            INNER JOIN vehicle g ON v.vehicle_id = g.vehicle_id
            INNER JOIN purpose o ON v.purpose_id = o.purpose_id
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
                sub_conditions.append("vehicle_type ILIKE %s")
                sub_conditions.append("purpose_type ILIKE%s")
                values.extend([f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"])
                search_conditions.append("(" + " OR ".join(sub_conditions) + ")")

            sql += " AND " + " AND ".join(search_conditions)

        # Add date range filter if provided
        if date_from and date_to:
            # Adjust end date by adding one day
            date_to_adjusted = (datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            sql += " AND date_requested BETWEEN %s AND %s"
            values.extend([date_from, date_to_adjusted])

        # Execute the query
        df = db.querydatafromdatabase(sql, values, columns_to_select)

        if df.shape[0]:  # Check if query returned anything
            # Fix column names
            df.columns = [
                "Vehicle Dispatch ID",
                "Request Number",
                "First Name",
                "Middle Initial",
                "Last Name",
                "Unit/Organization",
                "Email",
                "Contact Number",
                "Date Requested",
                "Date Started",
                "Vehicle Type",
                "Passenger Name/s",
                "Driver Name",
                "Purpose",
                "Destination",
                "Departure Date",
                "Departure Time",
                "Arrival Date",
                "Arrival Time",
                "Length of Trip",
                "Mode of Claiming",
                "Pickup Time",
                "Remarks",
                "Current Status",
                "Date Updated of Status",
                "Remarks on Status",
                "Request Class ID"
            ]

            ### ADD THIS BLOCK ###
            # Generate the "Edit" button for each request
            buttons = []
            for request_class_id in df['Request Class ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Update Request Status', href=f'/update_status_request?mode=edit&id={request_class_id}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            df = df.drop(columns=['Request Class ID'])  # Remove the ID column
            ### END OF BLOCK ###

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
    Output('download-dataframe-csv', 'data'),
    Input('btn_csv', 'n_clicks'),
    State('VDR_requestfilter', 'value'),
    State('date_from', 'date'),
    State('date_to', 'date'),
    prevent_initial_call=True
)
def download_csv(n_clicks, searchterm, date_from, date_to):
    # Define the columns you want to retrieve from the database
    columns_to_select = [
        "vehicle_dispatch_id",
        "request_number",
        "rc_first_name",
        "rc_middle_i",
        "rc_last_name",
        "organization",
        "email",
        "contact_number",
        "date_requested",
        "date_started",
        "vehicle_type",
        "passengers",
        "driver_name",
        "purpose_type",
        "destination",
        "borrow_date_from",
        "borrow_time_from",
        "borrow_date_to",
        "borrow_time_to",
        "length_of_trip",
        "mode_of_claiming",
        "pickup_time",
        "remarks_vehicledisp",
        "current_status", 
        "date_updated", 
        "remarks_statchange"

    ]

    # Base SQL query
    sql = f"""
        SELECT {', '.join(columns_to_select)}
        FROM vehicle_dispatch_request v
        INNER JOIN request_class r ON v.request_class_id = r.request_class_id
        INNER JOIN status_change s ON r.request_class_id = s.request_class_id
        INNER JOIN vehicle g ON v.vehicle_id = g.vehicle_id
        INNER JOIN purpose o ON v.purpose_id = o.purpose_id
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
                sub_conditions.append("vehicle_type ILIKE %s")
                sub_conditions.append("purpose_type ILIKE%s")
                values.extend([f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"])
                search_conditions.append("(" + " OR ".join(sub_conditions) + ")")

            sql += " AND " + " AND ".join(search_conditions)

    # Add date range filter if provided
    if date_from and date_to:
        # Adjust end date by adding one day
        date_to_adjusted = (datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        sql += " AND date_requested BETWEEN %s AND %s"
        values.extend([date_from, date_to_adjusted])

    # Execute the query
    df = db.querydatafromdatabase(sql, values, columns_to_select)

    if df.shape[0]:  # Check if query returned anything
        # Fix column names
        df.columns = [
            "Vehicle Dispatch ID",
            "Request Number",
            "First Name",
            "Middle Initial",
            "Last Name",
            "Unit/Organization",
            "Email",
            "Contact Number",
            "Date Requested",
            "Date Started",
            "Vehicle Type",
            "Passenger Name/s",
            "Driver Name",
            "Purpose",
            "Destination",
            "Departure Date",
            "Departure Time",
            "Arrival Date",
            "Arrival Time",
            "Length of Trip",
            "Mode of Claiming",
            "Pickup Time",
            "Remarks",
            "Current Status",
            "Date Updated of Status",
            "Remarks on Status"
        ]

        # Use StringIO to save the dataframe to a CSV string
        csv_string = StringIO()
        df.to_csv(csv_string, index=False)
        csv_string.seek(0)
        
        return dict(content=csv_string.getvalue(), filename="vehicle_dispatch_requests.csv")

    raise PreventUpdate

@app.callback(
    Output('date_from', 'date'),
    Output('date_to', 'date'),
    Input('clear_date_filter', 'n_clicks'),
    prevent_initial_call=True
)
def clear_date_filters(n_clicks):
    # Reset both date inputs to None
    return None, None
