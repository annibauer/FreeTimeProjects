import dash_bootstrap_components as dbc
from dash import html, dcc
from storage.settings import project_status_array


overview_button_group = dbc.Row([
    dbc.Col([], width=5),
    dbc.Col([
        dbc.ButtonGroup([
            dbc.Button(dbc.Row([dbc.Col([html.I(className="bi bi-plus")], width=1),dbc.Col(["New Project"], width=10)]), id="new_project_btn", className="me-1", n_clicks=0),
            dbc.Button(dbc.Row([dbc.Col([html.I(className="bi bi-pen")], width=1),dbc.Col(["Edit Project"], width=10)]), id="edit_project_info_btn", className="me-1", n_clicks=0),
            dbc.Button(dbc.Row([dbc.Col([html.I(className="bi bi-trash3-fill")], width=1),dbc.Col(["Delete Project"], width=10)]), id="delete_project_info_btn",  n_clicks=0)
        ])
        ], width=7)
])


project_cards_overview_element = dbc.Row(id='project_cards_overview', style={"margin":"20px"})