# Dash related dependencies
# To open browser upon running your app
import webbrowser

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Importing your app definition from app.py so we can use it
from app import app
from apps import commonmodules as cm
from apps import home, user, login, update_status_request, contactus, signup, view_request, view_cc_list, procurement_list
from apps.functions import add_cc, firstpage_vdr, firstpage_cc, vehicledispatchrequest, procurement, check_request_cc, check_request_vdr, firstpage_p, check_request_home

CONTENT_STYLE = {
    "margin-top": "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}
server = app.server
app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),
       
       
        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
       
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
       
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
       
        # Adding the navbar
        html.Div(
            cm.sidebar,
            id='navbar_div'
        ),


        # Page Content -- Div that contains page layout
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

@app.callback(
    [
        Output('navbar_div', 'children'),
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname'),
        Input('currentuserid', 'data'),
        Input('currentrole', 'data'),
    ]
)
def displaypage(pathname, currentuserid, currentrole):
    navbar = None
    page_content = None
    sessionlogout = False

    if currentuserid > 0:  # User is logged in
        if currentrole == 'Admin':
            if pathname == '/procurement_list':
                navbar = html.Div(cm.adminloginsidebar)
                page_content = procurement_list.layout
            elif pathname == '/user':
                navbar = html.Div(cm.adminloginsidebar)
                page_content = user.layout    
            elif pathname == '/signup':
                navbar = html.Div(cm.adminloginsidebar)
                page_content = signup.layout
            elif pathname == '/functions/firstpage_p':
                navbar = html.Div(cm.adminloginsidebar)
                page_content = firstpage_p.layout
            elif pathname == '/functions/procurement':
                navbar = html.Div(cm.adminloginsidebar)
                page_content = procurement.layout
            elif pathname == '/logout':
                navbar = html.Div(cm.sidebar)  # Set the navbar to sidebar when logging out
                page_content = login.layout
                sessionlogout = True
            elif pathname == '/view_request':
                navbar = html.Div(cm.adminloginsidebar)
                page_content = view_request.layout
            elif pathname == '/view_cc_list':
                navbar = html.Div(cm.adminloginsidebar)
                page_content = view_cc_list.layout
            elif pathname == '/update_status_request':
                navbar = html.Div(cm.adminloginsidebar)
                page_content = update_status_request.layout
            else:
                navbar = html.Div(cm.sidebar)
                page_content = home.layout
        else:
            if pathname == '/procurement_list':
                navbar = html.Div(cm.loginsidebar)
                page_content = procurement_list.layout
            elif pathname == '/user':
                navbar = html.Div(cm.loginsidebar)
                page_content = user.layout    
            elif pathname == '/functions/firstpage_p':
                navbar = html.Div(cm.loginsidebar)
                page_content = firstpage_p.layout
            elif pathname == '/functions/procurement':
                navbar = html.Div(cm.loginsidebar)
                page_content = procurement.layout
            elif pathname == '/logout':
                navbar = html.Div(cm.sidebar)  # Set the navbar to sidebar when logging out
                page_content = login.layout
                sessionlogout = True
            elif pathname == '/view_request':
                navbar = html.Div(cm.loginsidebar)
                page_content = view_request.layout
            elif pathname == '/view_cc_list':
                navbar = html.Div(cm.loginsidebar)
                page_content = view_cc_list.layout
            elif pathname == '/update_status_request':
                navbar = html.Div(cm.loginsidebar)
                page_content = update_status_request.layout
            else:
                navbar = html.Div(cm.sidebar)
                page_content = home.layout

    else:  # User is not logged in
        if pathname in ['/', '/home', '/check_request_home',
                        '/functions/check_request_cc',
                        '/functions/check_request_vdr',
                        '/functions/firstpage_vdr',
                        '/functions/firstpage_cc',
                        '/contactus', '/view_request', '/login','/functions/add_cc', '/functions/vehicledispatchrequest', '/functions/procurement']:
            if pathname == '/contactus':
                navbar = html.Div(cm.sidebar)
                page_content = contactus.layout
            elif pathname == '/login':
                navbar = html.Div(cm.sidebar)
                page_content = login.layout
            elif pathname == '/view_request':
                navbar = html.Div(cm.sidebar)
                page_content = view_request.layout
            elif pathname == '/functions/firstpage_vdr':
                navbar = html.Div(cm.sidebar)
                page_content = firstpage_vdr.layout
            elif pathname == '/functions/firstpage_cc':
                navbar = html.Div(cm.sidebar)
                page_content = firstpage_cc.layout
            elif pathname == '/functions/add_cc':
                navbar = html.Div(cm.sidebar)
                page_content = add_cc.layout
            elif pathname == '/functions/vehicledispatchrequest':
                navbar = html.Div(cm.sidebar)
                page_content = vehicledispatchrequest.layout
            elif pathname == '/functions/procurement':
                navbar = html.Div(cm.sidebar)
                page_content = procurement.layout
            elif pathname == '/check_request_home':
                navbar = html.Div(cm.sidebar)
                page_content = check_request_home.layout
            elif pathname == '/functions/check_request_cc':
                navbar = html.Div(cm.sidebar)
                page_content = check_request_cc.layout
            elif pathname == '/functions/check_request_vdr':
                navbar = html.Div(cm.sidebar)
                page_content = check_request_vdr.layout
            else:
                navbar = html.Div(cm.sidebar)
                page_content = home.layout
    
    return navbar, page_content, sessionlogout

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=False)
    app.run_server(debug=False)
