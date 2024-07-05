# Standard library imports
import csv
import glob
import json
import os
import warnings
from datetime import datetime, timedelta
from itertools import product

# Third-party imports
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback, callback_context, ctx, dcc, html
from dash.dependencies import Input, Output

# Config import
from dashboard.config import (
    critical_color,
    encoding_format,
    fail_color,
    folder_path_overview,
    high_color,
    info_color,
    informational_color,
    low_color,
    manual_color,
    medium_color,
    muted_fail_color,
    muted_manual_color,
    muted_pass_color,
    pass_color,
)
from dashboard.lib.cards import create_provider_card
from dashboard.lib.dropdowns import (
    create_account_dropdown,
    create_date_dropdown,
    create_region_dropdown,
    create_service_dropdown,
    create_severity_dropdown,
    create_status_dropdown,
    create_table_row_dropdown,
)
from dashboard.lib.layouts import create_layout_overview

# Suppress warnings
warnings.filterwarnings("ignore")

# Global variables
# TODO: Create a flag to let the user put a custom path
csv_files = []

for file in glob.glob(os.path.join(folder_path_overview, "*.csv")):
    with open(file, "r", newline="", encoding=encoding_format) as csvfile:
        reader = csv.reader(csvfile)
        num_rows = sum(1 for row in reader)
        if num_rows > 1:
            csv_files.append(file)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define login layout
login_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Login"), width=12)
        ]),
        dbc.Row([
            dbc.Col(html.Div("Username:"), width=3),
            dbc.Col(dcc.Input(id='username', type='text', placeholder='Enter username'), width=9)
        ]),
        dbc.Row([
            dbc.Col(html.Div("Password:"), width=3),
            dbc.Col(dcc.Input(id='password', type='password', placeholder='Enter password'), width=9)
        ]),
        dbc.Row([
            dbc.Col(html.Button('Login', id='login-button'), width=12)
        ])
    ])
])

# Define callback for handling login
@app.callback(
    Output('url', 'pathname'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')])
def login(n_clicks, username, password):
    if n_clicks > 0:
        # Perform login authentication here
        # For simplicity, let's assume authentication is successful
        return '/overview'  # Redirect to overview page upon successful login

# Define overview layout
overview_layout = create_layout_overview()  # Assuming you have a function to create overview layout

# Define app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Define callback to switch between pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/overview':
        return overview_layout
    else:
        return login_layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

