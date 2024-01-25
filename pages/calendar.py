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
from datetime import date
import numpy as np

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import calendar

from front_end.modals import add_event_modal
from functions.event import Event
from functions.storage_functions import extract_information_df, read_stored_events_information, read_stored_information
from storage.settings import json_storage_file, local_media_directiory, json_events_file, productive_hours
from functions.project_info_processing import add_new_event

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
    events_df = read_stored_events_information(json_events_file)
    
    for week in cal:
        week_row = []
        
        for day in week:
            if day == 0:
                week_row.append(dbc.Card([dbc.CardBody([])],style={"margin": "5px","width": "100%"}))
            else:
            
                if(len(str(month)) != 2):
                    month = '0'+ str(month)
                if(len(str(day)) != 2):
                    day = '0'+str(day)                 
                try:
                    day_events = events_df.loc[events_df['event_date'] == str(year)+"-"+str(month)+"-"+str(day)]
                    events_names = day_events.filter(items=['project_name','description']) 
                    progress_value = (np.sum(day_events['duration'].values)/productive_hours) * 100
                except Exception as error:
                    logging.debug("f Reading Json file error:  {error}")
                    events_names = pd.DataFrame({}, columns=['project_name','description'])
                    progress_value = 0
                    
                week_row.append(dbc.Card(
                    [
                        dbc.CardHeader(f"{day}", style={'padding':'0px 0px 0px 10px','margin':'5px'}),
                        dbc.CardBody(
                            [
                                dbc.Progress(value=progress_value, style={"height": "10px"}),
                                html.Ul([html.Li(x['project_name'] + " - " + x['description']) for i,x in events_names.iterrows()], style={'font-size':'60%','margin':'10px'})
                            ], style={'padding':'10px'}
                        ),

                    ],
                    style={"margin": "5px","width": "100%"}
                ))
                   
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
        dbc.Col([dbc.Button("Add Event", id="modal_add_event_btn", color="primary", className="mt-2", n_clicks=0)], width=8),
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
    ]),
    add_event_modal
], style={'margin':'20px'})

@callback([
    Output('calendar-container', 'children'),
    Output('month_year_displayed', 'children'),
    Output('output_date_picker_add_event', 'children'),
    Output('add_event_btn', 'n_clicks')
    ],[
    Input('month-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    State('date-picker-add-event', 'date'),
    State('select_event_projects_dropdown', 'value'),
    State('event_description', 'value'),
    State('hours_event_dropdown', 'value'),
    Input('add_event_btn', 'n_clicks') 
    ]
)
def update_calendar(selected_month, selected_year, date_value, project_name_event, event_descrption, hours_event, n_clicks_add_event):
    month_name = calendar.month_name[selected_month]
    title_displayed = str(month_name) + " " + str(selected_year)
    
    string_prefix = 'You have selected: '
    date_selected = ''

    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        date_selected = string_prefix + date_string
    if n_clicks_add_event != 0 and project_name_event != None :
        
        add_new_event(json_storage_file, json_events_file, project_name_event,date_value, event_descrption, hours_event)
        list_of_cards, project_names, project_ids = extract_information_df(json_storage_file)

    n_clicks_add_event = 0  
    
    return generate_calendar(selected_year, selected_month), title_displayed, date_selected, n_clicks_add_event

@callback([
    Output('modal_add_event_btn', 'n_clicks'),
    Output('modal_add_event', 'is_open'),
    Output('select_event_projects_dropdown', 'options'),
    Output('select_event_projects_dropdown', 'value'),
    Output('date-picker-add-event', 'initial_visible_month'),
    Output('date-picker-add-event', 'date'),
    Output('hours_event_dropdown', 'options')
    ],[Input('modal_add_event_btn', 'n_clicks'),
       Input('add_event_btn', 'n_clicks'),
        State('month-dropdown', 'value'),
        State('year-dropdown', 'value')]
)
def open_event_modal(n_add_event_modal, add_event_btn ,  month, year):
    list_of_cards, project_names, project_ids = extract_information_df(json_storage_file)

    try:
        first_project = project_names[0]
    except:
        first_project = ''
        
    intial_month = date(year=year,month=month,day=date.today().day)
    initial_day = date.today()
    
    options_time = [x * 0.25 for x in range(0, 30)]
    if(n_add_event_modal != 0):
        modal_visible = True
    elif(add_event_btn !=0):
        modal_visible = False
    else:
        modal_visible = False
    
    n_add_event_modal = 0
    return n_add_event_modal, modal_visible, project_names, first_project, intial_month, initial_day,  options_time