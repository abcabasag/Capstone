import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
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
        html.H2('Procurement'),  # Page Header
        html.Hr(),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    [
                        html.H3('Manage Records of Procurement Requests')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        dbc.Row(
                            [
                                dbc.Label("Add", style={"color": "white"}),
                                dbc.Col(
                                    dbc.Button("Add Procurement Request",
                                               id='addprocurement_btn',
                                               href='/functions/firstpage_p',
                                               # outline=True,
                                               color="dark"
                                               ), width=3)
                            ]
                        ),
                        html.Hr(),
                        html.Div(  # Create section to show list of movies
                            [
                                html.H4('Find Procurement Request'),
                                dbc.Form(
                                    dbc.Row(
                                        [
                                            dbc.Label("Search Request", width=1),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id='pr_requestfilter',
                                                    placeholder='Request Number, Requestor First Name, Requestor Last Name, or Item'
                                                ),
                                                width=5
                                            ),
                                            dbc.Label("Filter by Date Requested:", width=2),
                                            dbc.Col(
                                                dcc.DatePickerSingle(
                                                    id='prdate_from',
                                                    placeholder='Start Date',
                                                    style={'width': '130px', 'font-size': '12px'}
                                                ),
                                                width='auto'
                                            ),
                                            dbc.Label("to", width='auto', style={'text-align': 'center', 'padding-top': '10px'}),
                                            dbc.Col(
                                                dcc.DatePickerSingle(
                                                    id='prdate_to',
                                                    placeholder='End Date',
                                                    style={'width': '130px', 'font-size': '12px'}
                                                ),
                                                width='auto'
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "X",
                                                    id='prclear_date_filter',
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
                                            dbc.Button("Export CSV", id="prbtn_csv", color="primary"),
                                            width='auto'
                                        ),
                                        dcc.Download(id="prdownload-dataframe-csv")
                                    ],
                                    className='mb-3 align-items-center'
                                ),
                                html.Div(id='prrow_count'),  # Row count display here
                                html.Div(
                                        "Table with procurement requests will go here.",
                                        id='pr_requestlist'
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
        Output('pr_requestlist', 'children'),
        Output('prrow_count', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('pr_requestfilter', 'value'),  # changing the text box value should update the table
        Input('prdate_from', 'date'),  # Start date for the date range filter
        Input('prdate_to', 'date')  # End date for the date range filter
    ]
)
def procurement_load_request_list(pathname, searchterm, prdate_from, prdate_to):
    if pathname == '/procurement_list':
        # Define the columns you want to retrieve from the database
        PRcolumns_to_select = [
            "procurement_id",
            "request_number",
            "rc_first_name",
            "rc_middle_i",
            "rc_last_name",
            "organization",
            "date_requested",
            "date_needed",
            "date_started",
            "item",
            "quantity",
            "additional_remarks_procu",
            "current_status", 
            "date_updated", 
            "remarks_statchange",
            "r.request_class_id"
        ]

        # Base SQL query
        sql = f"""
            SELECT {', '.join(PRcolumns_to_select)}
            FROM procurement_request p
            INNER JOIN request_class r ON p.request_class_id = r.request_class_id
            INNER JOIN status_change s ON r.request_class_id = s.request_class_id
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
                sub_conditions.append("item ILIKE %s")
                values.extend([f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"])
                search_conditions.append("(" + " OR ".join(sub_conditions) + ")")

            sql += " AND " + " AND ".join(search_conditions)
        # Add date range filter if provided
        if prdate_from and prdate_to:
            # Adjust end date by adding one day
            date_to_adjusted = (datetime.strptime(prdate_to, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            sql += " AND date_requested BETWEEN %s AND %s"
            values.extend([prdate_from, date_to_adjusted])

        # Execute the query
        df = db.querydatafromdatabase(sql, values, PRcolumns_to_select)

        if df.shape[0]:  # Check if query returned anything
            # Fix column names
            df.columns = [
                "Procurement Request ID",
                "Request Number",
                "First Name",
                "Middle Initial",
                "Last Name",
                "Unit/Organization",
                "Date Requested",
                "Date Needed",
                "Date Started",
                "Item",
                "Quantity",
                "Remarks/Specifications",
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
    Output('prdownload-dataframe-csv', 'data'),
    Input('prbtn_csv', 'n_clicks'),
    State('pr_requestfilter', 'value'),
    State('prdate_from', 'date'),
    State('prdate_to', 'date'),
    prevent_initial_call=True
)
def prdownload_csv(n_clicks, searchterm, prdate_from, prdate_to):
    # Define the columns you want to retrieve from the database
    PRcolumns_to_select = [
        "procurement_id",
        "request_number",
        "rc_first_name",
        "rc_middle_i",
        "rc_last_name",
        "organization",
        "date_requested",
        "date_needed",
        "date_started",
        "item",
        "quantity",
        "additional_remarks_procu",
        "current_status", 
        "date_updated", 
        "remarks_statchange",
    ]

    # Base SQL query
    sql = f"""
        SELECT {', '.join(PRcolumns_to_select)}
        FROM procurement_request p
        INNER JOIN request_class r ON p.request_class_id = r.request_class_id
        INNER JOIN status_change s ON r.request_class_id = s.request_class_id
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
                sub_conditions.append("item ILIKE %s")
                values.extend([f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%"])
                search_conditions.append("(" + " OR ".join(sub_conditions) + ")")

            sql += " AND " + " AND ".join(search_conditions)

    # Add date range filter if provided
    if prdate_from and prdate_to:
        # Adjust end date by adding one day
        date_to_adjusted = (datetime.strptime(prdate_to, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        sql += " AND date_requested BETWEEN %s AND %s"
        values.extend([prdate_from, date_to_adjusted])

    # Execute the query
    df = db.querydatafromdatabase(sql, values, PRcolumns_to_select)

    if df.shape[0]:  # Check if query returned anything
        # Fix column names
        df.columns = [
            "Procurement Request ID",
                "Request Number",
                "First Name",
                "Middle Initial",
                "Last Name",
                "Unit/Organization",
                "Date Requested",
                "Date Needed",
                "Date Started",
                "Item",
                "Quantity",
                "Remarks/Specifications",
                "Current Status",
                "Date Updated of Status",
                "Remarks on Status",
        ]

        # Use StringIO to save the dataframe to a CSV string
        csv_string = StringIO()
        df.to_csv(csv_string, index=False)
        csv_string.seek(0)
        
        return dict(content=csv_string.getvalue(), filename="procurement_requests.csv")

    raise PreventUpdate

@app.callback(
    Output('prdate_from', 'date'),
    Output('prdate_to', 'date'),
    Input('prclear_date_filter', 'n_clicks'),
    prevent_initial_call=True
)
def prclear_date_filters(n_clicks):
    # Reset both date inputs to None
    return None, None
