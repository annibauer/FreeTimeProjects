import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import calendar
import dash
from dash import Dash, html, dcc, html, Input, Output, callback, State
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import dash_bootstrap_components as dbc
import geocoder as gc
from pprint import pprint
import json
import os
from os import listdir
from os.path import isfile, join
import logging

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import calendar

dash.register_page(__name__)


def generate_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    weeks = []
    
    # generate week day titles
    week_days_name = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
    week_row_title = []
    for weekday in week_days_name:
            week_row_title.append(dbc.Card(
                [html.H6(weekday,style={'text-align':'center','margin':'10px'})],
                style={"margin": "5px","width": "100%","height":"100%"}
            ))
            
    weeks.append(html.Div(week_row_title, className="d-flex justify-content-center"))
    
    for week in cal:
        week_row = []
        
        for day in week:
            if day == 0:
                week_row.append(dbc.Card([dbc.CardBody([])],style={"margin": "5px","width": "100%"}))
            else:
                events = []  # List to store events for the current day
                week_row.append(dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.P(f"{day}"),
                                html.Div(id=f"events-{year}-{month}-{day}")
                            ]
                        ),
                        # dbc.Input(id=f"event-input-{year}-{month}-{day}", type="text", placeholder="Add event"),
                        # dbc.Button("Add Event", id=f"add-event-btn-{year}-{month}-{day}", color="primary", className="mt-2"),
                    ],
                    style={"margin": "5px","width": "100%"}
                ))
                
                # @callback(
                #     Output(f"events-{year}-{month}-{day}", "children"),
                #     [Input(f"add-event-btn-{year}-{month}-{day}", "n_clicks")],
                #     [Input(f"event-input-{year}-{month}-{day}", "value")]
                # )
                # def add_event(n_clicks, event_text):
                #     if n_clicks is None:
                #         raise dash.exceptions.PreventUpdate
                #     print(event_text)
                #     events.append(html.Li(event_text))
                #     return events
        
        # Fill up the week with empty dbc.Card elements for days before the first day of the month
        if len(week_row) < 7 and cal.index(week) == 0:
            week_row = [html.Div()] * (7 - len(week_row)) + week_row
        
        # Fill up the week with empty dbc.Card elements for days after the last day of the month
        elif len(week_row) < 7 and cal.index(week) == len(cal) - 1:
            week_row += [html.Div()] * (7 - len(week_row))
        
        weeks.append(html.Div(week_row, className="d-flex justify-content-center"))

    return html.Div(weeks, className="d-flex flex-column")

layout = html.Div([
    dbc.Row([
        html.H1(id="month_year_displayed",children=["Monthly Calendar with Events"], style={'margin':'5px'})
        ]),
    dbc.Row([
        dbc.Col([], width=8),
        dbc.Col([    
                 dcc.Dropdown(
        id='month-dropdown',
        options=[
            {'label': calendar.month_name[i], 'value': i} for i in range(1, 13)
        ],
        value=datetime.now().month,
        style={"width": "100%", "color":"black"})
        ]),
        dbc.Col([
            dcc.Dropdown(
                id='year-dropdown',
                options=[
                    {'label': i, 'value': i} for i in range(2022, 2030)
                ],
                value=datetime.now().year,
                style={"width": "100%", "color":"black"})
            ])
        ], style={'margin-bottom':'10px'}),
    dbc.Row([
        html.Div(id='calendar-container'),    
    ])
], style={'margin':'20px'})

@callback([
    Output('calendar-container', 'children'),
    Output('month_year_displayed', 'children')
    ],[
    Input('month-dropdown', 'value'),
    Input('year-dropdown', 'value')]
)
def update_calendar(selected_month, selected_year):
    month_name = calendar.month_name[selected_month]
    title_displayed = str(month_name) + " " + str(selected_year)
    
    return generate_calendar(selected_year, selected_month), title_displayed


