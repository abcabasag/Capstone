# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app
#for DB needs
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Button(html.Img(src='/assets/back.svg'),
                   id='back_button',
                   href='/home',  # Adjust this URL to match your home page URL
                   outline=True,
                   color="light"
                   ),
        html.H2('Request Status Viewer'), # Page Header
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Find Request Status here')
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Hr(),
                        html.Div( # Create section to show list of movies
                            [
                                dbc.Form(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='checkrequestfilter',
                                                        placeholder='Type your Request Number here.'
                                                    ),
                                                    width=5
                                                ),
                                                dbc.Col(
                                                    dbc.Button("Search", id="search_button", color="primary"),
                                                    width=1,
                                                ),
                                            ],
                                            className = 'mb-3'
                                        ),
                                        html.Div(
                                            "Please input a Request Number",
                                            id='checkrequestlist'
                                        )
                                    ]
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
    Output('checkrequestlist', 'children'),
    [Input('search_button', 'n_clicks')],
    [State('checkrequestfilter', 'value')],
)
def update_search_results(n_clicks, searchterm):
    if n_clicks is None:
        raise PreventUpdate

    # Query the database based on search term
    sql = """ SELECT request_number, current_status, date_updated, remarks_statchange
            FROM request_class m
            INNER JOIN status_change g ON m.request_class_id = g.request_class_id
        """
    values = [] # blank since I do not have placeholders in my SQL
    cols = ['Request Number', 'Status', 'Date Updated', 'Remarks']

    if searchterm:
        # Add filter condition if search term is provided
        sql += " WHERE request_number LIKE %s"
        values += [f"{searchterm}"]

    df = db.querydatafromdatabase(sql, values, cols)

    if not df.empty:
        # If records are found, return table
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return [table]
    else:
        # If no records found, return message
        return ["No records found."]
