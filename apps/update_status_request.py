from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app
from urllib.parse import parse_qs
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Button(
            html.Img(src='/assets/back.svg'),
            id='back_button',
            href='/user',
            outline=True,
            color="light",
            style={"margin-bottom": "10px"}
        ),
        html.H2('Update Status of Request', style={"color": "#0056b3"}),
        html.Hr(),
        dbc.Alert(id='gen_alert', is_open=False),
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Status", width=1, style={"color": "#0056b3"}),
                        dbc.Col(
                            dcc.Dropdown(
                                id='status_dropdown',
                                options=[
                                    {'label': 'Pending', 'value': 'Pending'},
                                    {'label': 'Approved', 'value': 'Approved'},
                                    {'label': 'Ongoing', 'value': 'Ongoing'},
                                    {'label': 'Completed', 'value': 'Completed'},
                                    {'label': 'Rejected', 'value': 'Rejected'}
                                ],
                                placeholder='Select status',
                                style={"border": "1px solid #0056b3"}  # Blue border for dropdown
                            ),
                            width=4
                        )
                    ],
                    style={"margin-bottom": "20px"}
                ),
                dbc.Row(
                    [
                        dbc.Label("Remarks", width=1, style={"color": "#0056b3"}),
                        dbc.Col(
                            dcc.Textarea(
                                id='gen_remarks',
                                placeholder='Remarks',
                                style={'width': '100%', "border": "1px solid #0056b3"}  # Blue border for textarea
                            ),
                            width=5,
                        )
                    ],
                    className='mb-3 align-items-center',
                    style={"margin-bottom": "20px"}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                'Update Status',  # Changed button label
                                id='gen_submit',
                                n_clicks=0,
                                color="primary",
                                style={"width": "100%"}
                            ),
                            width={"size": 2, "offset": 5}
                        )
                    ],
                ),
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Submission Successful', style={"color": "#0056b3"})
                ),
                dbc.ModalBody(
                    html.Div(
                        'Your Status has been successfully updated.',
                        style={'text-align': 'center'}
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Finish",
                        href='/user',
                        color="primary"
                    )
                )
            ],
            centered=True,
            id='gen_successmodal',
            backdrop='static'
        )
    ],
    style={"maxWidth": "1600px", "margin-left": "220px"}
)

@app.callback(
    Output('gen_successmodal', 'is_open'),
    Output('gen_alert', 'children'),
    Output('gen_alert', 'color'),
    Output('gen_alert', 'is_open'),
    Input('gen_submit', 'n_clicks'),
    [
        State('url', 'search'),
        State('status_dropdown', 'value'),
        State('gen_remarks', 'value'),
        State('currentuserid', 'data')  # Get the user ID from session data
    ]
)
def update_status(n_clicks, search, selected_status, remarks, currentuserid):
    if n_clicks == 0:
        raise PreventUpdate

    if not selected_status and not remarks:
        return False, "Please select a status and input remarks.", "danger", True
    elif not selected_status:
        return False, "Please select a status.", "danger", True
    elif not remarks:
        return False, "Please input remarks.", "danger", True

    request_class_id = parse_qs(search)['id'][0]

    if selected_status == "Approved":
        update_status_query = """
        UPDATE Status_Change 
        SET Current_Status = %s, 
            Date_Started = CURRENT_DATE,
            Date_updated = CURRENT_DATE, 
            Remarks_statchange = %s,
            Status_ID = (SELECT Status_ID FROM Status WHERE Status_Name = %s),
            user_id = %s  -- Store the user ID who made the change
        WHERE Request_Class_ID = %s;
        """
        db.modifydatabase(update_status_query, [selected_status, remarks, selected_status, currentuserid, request_class_id])
    else:
        update_status_query = """
        UPDATE Status_Change 
        SET Current_Status = %s, 
            Date_updated = CURRENT_DATE, 
            Remarks_statchange = %s,
            Status_ID = (SELECT Status_ID FROM Status WHERE Status_Name = %s),
            user_id = %s  -- Store the user ID who made the change
        WHERE Request_Class_ID = %s;
        """
        db.modifydatabase(update_status_query, [selected_status, remarks, selected_status, currentuserid, request_class_id])

    return True, "", "", False

