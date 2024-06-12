from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from apps import dbconnect as db

layout = html.Div([
    html.Div([
        dbc.Card([
            dbc.CardHeader([
                html.H3("Hello, "), 
                html.H3(id='session-user-name')  # Display the user's name here
            ], className='flex'),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(html.Strong("Procurement Request List", style={'text-align': 'center', 'font-size': '24px', 'font-weight': 'bold'})),
                            dbc.CardBody([
                                html.Div(id='status-counts-prc', className='status-counts'),
                                html.Div(id='pie-prc', children=dcc.Graph(id='prc-pie-chart')),
                            ]),
                            dbc.CardFooter(
                                dbc.Row(
                                    dbc.Button("Check Procurement Request List", href="/procurement_list", color="primary", className="mr-1 text-center"),
                                    justify="center"
                                )
                            ),
                        ]),
                        width=4  # Adjust the width for proper alignment
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(html.Strong("Vehicle Dispatch Request List", style={'text-align': 'center', 'font-size': '24px', 'font-weight': 'bold'})),
                            dbc.CardBody([
                                html.Div(id='status-counts-vdr', className='status-counts'),
                                html.Div(id='pie-vdr', children=dcc.Graph(id='vdr-pie-chart')),
                            ]),
                            dbc.CardFooter(
                                dbc.Row(
                                    dbc.Button("Check Vehicle Dispatch Request List", href="/view_request", color="primary", className="mr-1 text-center"),
                                    justify="center"
                                )
                            ),
                        ]),
                        width=4  # Adjust the width for proper alignment
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(html.Strong("Citizens Charter Request List", style={'text-align': 'center', 'font-size': '24px', 'font-weight': 'bold'})),
                            dbc.CardBody([
                                html.Div(id='status-counts-cc', className='status-counts'),
                                html.Div(id='pie-cc', children=dcc.Graph(id='cc-pie-chart')),
                            ]),
                            dbc.CardFooter(
                                dbc.Row(
                                    dbc.Button("Check Citizens Charter Request List", href="/view_cc_list", color="primary", className="mr-1 text-center"),
                                    justify="center"
                                )
                            ),
                        ]),
                        width=4  # Adjust the width for proper alignment
                    ),
                ], className="align-items-start justify-content-center"),
            ])
        ])
    ], className='flex body-container')
], style={'max-width': '1500px', 'margin-left': '220px'})

# Update the user's name callback
@app.callback(
    Output('session-user-name', 'children'),
    [Input('url', 'pathname')],
    [State('currentuserid', 'data')]
)
def update_session_user_name(pathname, currentuserid):
    if currentuserid:
        sql = """SELECT First_Name, Last_Name
                 FROM users
                 WHERE user_id = %s"""
        values = [currentuserid]
        cols = ['First_Name', 'Last_Name']
        df = db.querydatafromdatabase(sql, values, cols)
        if not df.empty:
            first_name = df['First_Name'][0]
            last_name = df['Last_Name'][0]
            return f"{first_name} {last_name}"
        else:
            return "User"  # Default text if user data is not found
    else:
        return "User"  # Default text if session data is not available

# Update card headers with status counts
@app.callback(
    [
        Output('status-counts-prc', 'children'),
        Output('status-counts-vdr', 'children'),
        Output('status-counts-cc', 'children'),
        Output('prc-pie-chart', 'figure'),
        Output('vdr-pie-chart', 'figure'),
        Output('cc-pie-chart', 'figure'),
    ],
    [Input('url', 'pathname')],
    [State('currentuserid', 'data')]
)
def update_total_counts(pathname, currentuserid):
    if pathname == "/user" and currentuserid:
        # Query the counts of different statuses for procurement requests
        status_prc_sql = """
            SELECT s.Status_Name, COUNT(*)
            FROM Status_Change sc
            JOIN Status s ON sc.Status_ID = s.Status_ID
            JOIN Procurement_Request pr ON sc.Request_Class_ID = pr.Request_Class_ID
            WHERE (pr.Procurement_Request_Delete IS NULL OR pr.Procurement_Request_Delete = False)
            AND sc.current_ind = True
            GROUP BY s.Status_Name
        """
        status_prc_df = db.querydatafromdatabase(status_prc_sql, [], ['Status_Name', 'count'])

        # Query the counts of different statuses for vehicle dispatch requests
        status_vdr_sql = """
            SELECT s.Status_Name, COUNT(*)
            FROM Status_Change sc
            JOIN Status s ON sc.Status_ID = s.Status_ID
            JOIN Vehicle_Dispatch_Request vdr ON sc.Request_Class_ID = vdr.Request_Class_ID
            WHERE (vdr.Vehicle_Dispatch_Request_Delete IS NULL OR vdr.Vehicle_Dispatch_Request_Delete = False)
            AND sc.current_ind = True
            GROUP BY s.Status_Name
        """
        status_vdr_df = db.querydatafromdatabase(status_vdr_sql, [], ['Status_Name', 'count'])

        # Query the counts of different statuses for citizens charter requests
        status_cc_sql = """
            SELECT s.Status_Name, COUNT(*)
            FROM Status_Change sc
            JOIN Status s ON sc.Status_ID = s.Status_ID
            JOIN Citizen_Charter_Request cc ON sc.Request_Class_ID = cc.Request_Class_ID
            WHERE (cc.Citizen_Charter_Request_Delete IS NULL OR cc.Citizen_Charter_Request_Delete = False)
            AND sc.current_ind = True
            GROUP BY s.Status_Name
        """
        status_cc_df = db.querydatafromdatabase(status_cc_sql, [], ['Status_Name', 'count'])

        # Initialize status counts
        status_counts_prc = {
            'Pending': 0,
            'Approved': 0,
            'Ongoing': 0,
            'Completed': 0,
            'Rejected': 0
        }
        status_counts_vdr = {
            'Pending': 0,
            'Approved': 0,
            'Ongoing': 0,
            'Completed': 0,
            'Rejected': 0
        }
        status_counts_cc = {
            'Pending': 0,
            'Approved': 0,
            'Ongoing': 0,
            'Completed': 0,
            'Rejected': 0
        }

        # Fill in the counts based on the query results
        for _, row in status_prc_df.iterrows():
            status_counts_prc[row['Status_Name']] = row['count']
        for _, row in status_vdr_df.iterrows():
            status_counts_vdr[row['Status_Name']] = row['count']
        for _, row in status_cc_df.iterrows():
            status_counts_cc[row['Status_Name']] = row['count']

        # Define custom colors for most elements
        custom_colors = px.colors.sequential.Blues

        # Override the color for a specific element
        override_color = 'rgb(255, 127, 14)'  # Orange color

        # Create pie charts
        prc_fig = px.pie(values=list(status_counts_prc.values()), 
                        names=list(status_counts_prc.keys()), 
                        title='Procurement Request Status',
                        color_discrete_sequence=custom_colors)
        # Change the color of a specific element (e.g., 'Rejected') in the pie chart
        prc_fig.update_traces(marker=dict(colors=[override_color if label == 'Pending' else None for label in prc_fig.data[0]['labels']]))

        vdr_fig = px.pie(values=list(status_counts_vdr.values()), 
                        names=list(status_counts_vdr.keys()), 
                        title='Vehicle Dispatch Request Status',
                        color_discrete_sequence=custom_colors)
        vdr_fig.update_traces(marker=dict(colors=[override_color if label == 'Pending' else None for label in vdr_fig.data[0]['labels']]))

        cc_fig = px.pie(values=list(status_counts_cc.values()), 
                        names=list(status_counts_cc.keys()), 
                        title='Citizen Charter Request Status',
                        color_discrete_sequence=custom_colors)
        cc_fig.update_traces(marker=dict(colors=[override_color if label == 'Pending' else None for label in cc_fig.data[0]['labels']]))

        # Create status count strings
        status_counts_prc_str = "\n".join([f"{key}: {value}" for key, value in status_counts_prc.items()])
        status_counts_vdr_str = "\n".join([f"{key}: {value}" for key, value in status_counts_vdr.items()])
        status_counts_cc_str = "\n".join([f"{key}: {value}" for key, value in status_counts_cc.items()])

        status_counts_prc_str = html.Pre(status_counts_prc_str)
        status_counts_vdr_str = html.Pre(status_counts_vdr_str)
        status_counts_cc_str = html.Pre(status_counts_cc_str)

        return (
                status_counts_prc_str, 
                status_counts_vdr_str, 
                status_counts_cc_str, 
                prc_fig, 
                vdr_fig, 
                cc_fig)
    else:
        return "", "", "", {}, {}, {}  # Default empty values if session or pathname is invalid
