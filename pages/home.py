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

from front_end.modals import new_project_modal_element, edit_project_modal_element, delete_project_modal_element
from front_end.overview import overview_button_group, project_cards_overview_element
from functions.project import Project
from functions.storage_functions import extract_information_df, read_stored_information
from functions.data_processing import transform_stored_data_links
from functions.project_info_processing import add_new_project, delete_project_with_name, save_edited_project, load_data_into_modal, add_image_to_new_project, add_general_link_to_new_project, add_steps_taken_to_new_project, add_steps_todo_to_new_project
from storage.settings import json_storage_file, local_media_directiory

dash.register_page(__name__, path='/')

layout = html.Div([
    overview_button_group,
    new_project_modal_element,
    edit_project_modal_element,
    delete_project_modal_element,
    project_cards_overview_element
  
],style={'textAlign': 'center', 'padding':'10px'})


# Open Modal To Enter Details For New Project
@callback([
    Output("new_project_modal", "is_open"),
    Output("new_project_btn","n_clicks"),    
    ], [Input("new_project_btn", "n_clicks"),
        Input("add_project_btn", "n_clicks")]
)
def project_modal(n_new, n_new_add):
    if n_new == 0:
        new_project_modal_visible = False
    else:
        new_project_modal_visible = True
    if(n_new_add !=0):
        new_project_modal_visible = False
    
    n_new = 0
    return new_project_modal_visible, n_new, 
    
    
    
    
# Manipulate Projects 
@callback([
    # project cards to display
    Output("project_cards_overview","children"),
    # buttons to reset after click
    Output("add_project_btn","n_clicks"),    
    Output("project_save_status","children"),
    Output("delete_project_btn", "n_clicks"),
    # Project Saved Status
    # # Reset new project inputs
    Output("input_new_project_name", "value"),
    Output("input_new_project_hobby", "value"),
    Output("input_new_project_notes", "value"),
    Output("dd_project_status", "value"),
    # load already saved data into input fields when editing project
    Output("save_project_btn","n_clicks"),
    Output("input_edit_project_name", "value"),
    Output("input_edit_project_hobby", "value"),
    Output("input_edit_project_notes", "value"),
    Output("dd_project_status_edit", "value"),
    Output("input_edit_images_table", "data"),
    Output("input_edit_links_table", "data"),
    Output("add_edit_image_btn", "n_clicks"),
    Output("add_edit_link_btn", "n_clicks"),
    Output("input_edit_steps_taken_table", "data"),
    Output("input_edit_steps_todo_table", "data"),
    Output("add_edit_steps_taken", "n_clicks"),
    Output("add_edit_todo", "n_clicks")
    ], [
        # trigger buttons
        Input("add_project_btn", "n_clicks"),
        Input("save_project_btn", "n_clicks"),
        Input("delete_project_btn", "n_clicks"),
        # displayed projects in div
        State("project_cards_overview","children"),
        # new project inputs
        State("input_new_project_name", "value"), 
        State("input_new_project_hobby", "value"),
        State("input_new_project_notes", "value"),
        State("dd_project_status", "value"),
        State("input_new_links_table", "data"),
        State("input_new_images_table", "data"),
        State("input_new_steps_taken_table", "data"),
        State("input_new_steps_todo_table", "data"),
        # edit project inputs
        Input("edit_projects_dropdown", "value"),
        State("input_edit_project_name", "value"),
        State("input_edit_project_hobby", "value"),
        State("input_edit_project_notes", "value"),
        State("dd_project_status_edit", "value"),
        State("input_edit_links_table", "data"),
        State("input_edit_images_table", "data"), 
        State("input_edit_steps_taken_table", "data"),
        State("input_edit_steps_todo_table", "data"),
        # delete project
        State("delete_projects_dropdown", "value"),
        # add image or normal url link for edit project
        Input("add_edit_image_btn", "n_clicks"),
        Input("add_edit_link_btn", "n_clicks"),
        State("input_edit_image_link", "value"),
        State("input_edit_links", "value"),
        Input("add_edit_steps_taken", "n_clicks"),
        Input("add_edit_todo", "n_clicks"),
        State("input_edit_steps_taken", "value"),
        State("input_edit_steps_todo", "value"),
       ]
    
)
def manipulate_project_info(n_new, n_edit_save, n_delete, list_of_cards, input_project_name, input_hobby_name, input_notes, project_status_input, input_links ,input_image_links, input_steps_taken, input_steps_todo, selected_project_to_edit, input_project_name_edit, input_hobby_name_edit, input_notes_edit, project_status_input_edit, input_links_edit, input_image_links_edit, input_steps_taken_edit , input_steps_todo_edit, selected_project_delete, n_image_edit, n_links_edit, image_link, url_link, n_steps_taken_edit, n_steps_todo_edit, input_step_taken, input_step_todo): 
    project_save_status = ''

    # WHEN SAVE NEW PROJECT PRESSED
    if n_new != 0:

        list_of_cards, project_names, n_new, project_save_status, input_project_name, input_hobby_name, input_notes, project_status_input = add_new_project(json_storage_file, input_project_name, input_hobby_name, project_status_input, input_notes, input_steps_taken, input_steps_todo, input_links, input_image_links)


    # WHEN DELETE PROJECT PRESSED
    elif(n_delete != 0 and selected_project_delete != None):
        delete_project_with_name(json_storage_file, selected_project_delete)     
        # reset delete project button
        n_delete = 0

        
    # if within edit project modal a project is selected to be edited    
    if(selected_project_to_edit != None):
        
        input_edit_project_name, input_edit_project_hobby, input_edit_project_notes, dd_project_status_edit, image_links_edit, links_edit, steps_taken_edit, steps_todo_edit = load_data_into_modal(json_storage_file,selected_project_to_edit)
        # add image link and save edited project
        if(n_image_edit != 0):
            list_of_cards, n_image_edit, image_links_edit, image_link = add_image_to_new_project(json_storage_file,  selected_project_to_edit,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_link, input_links_edit, input_steps_taken_edit, input_steps_todo_edit)
         # add general link and save edited project
        elif(n_links_edit != 0):
            list_of_cards, n_links_edit,links_edit, url_link = add_general_link_to_new_project(json_storage_file, selected_project_to_edit, input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, steps_taken_edit, steps_todo_edit)
        # add step taken to save edited project
        elif(n_steps_taken_edit != 0):            
            list_of_cards, n_steps_taken_edit, steps_taken_edit, input_step_taken = add_steps_taken_to_new_project(json_storage_file, selected_project_to_edit, input_step_taken ,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, links_edit,steps_todo_edit)              
        # add general link and save edited project
        elif(n_steps_todo_edit != 0):
            list_of_cards, n_steps_todo_edit, steps_todo_edit, input_step_todo = add_steps_todo_to_new_project(json_storage_file, selected_project_to_edit, input_step_todo, input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, links_edit, steps_taken_edit, steps_todo_edit)
        # save edited project pressed
        elif(n_edit_save != 0):
            list_of_cards, project_names  = save_edited_project(json_storage_file, selected_project_to_edit,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, links_edit, steps_taken_edit, steps_todo_edit)
            n_edit_save = 0
            
    else:
        # if no project is selected in edit modal dropdown set all inputs empty
        input_edit_project_name = ''
        input_edit_project_hobby = ''
        input_edit_project_notes = ''
        dd_project_status_edit = ''
        image_links_edit = pd.DataFrame().to_dict('records')
        links_edit = pd.DataFrame().to_dict('records')
        steps_taken_edit = pd.DataFrame().to_dict('records')
        steps_todo_edit = pd.DataFrame().to_dict('records')
        

    list_of_cards, project_names = extract_information_df(json_storage_file)
    
    return list_of_cards,  n_new, project_save_status , n_delete, input_project_name, input_hobby_name, input_notes, project_status_input, n_edit_save, input_edit_project_name, input_edit_project_hobby, input_edit_project_notes, dd_project_status_edit, image_links_edit, links_edit , n_image_edit, n_links_edit, steps_taken_edit, steps_todo_edit,  n_steps_taken_edit, n_steps_todo_edit
    
    
    
# Open Modal To Edit Details of existing Project
@callback([
    Output("edit_project_modal", "is_open"),
    Output("edit_projects_dropdown", "options"),
    Output("edit_projects_dropdown", "value"),
    Output("edit_project_info_btn","n_clicks")
    ], [
        Input("edit_project_info_btn", "n_clicks")
        ]
)
def edit_project_modal(n):
    if n == 0:
        edit_project_modal = False
        edit_projects_dropdown_options = []
        edit_projects_dropdown_value = None

    else:
        list_of_cards, project_names = extract_information_df(json_storage_file)
        edit_project_modal = True
        edit_projects_dropdown_options = project_names
        edit_projects_dropdown_value = project_names[0]
                
    edit_project_info_click = 0
    return edit_project_modal, edit_projects_dropdown_options, edit_projects_dropdown_value , edit_project_info_click 
    

# Open Modal To Delete Project
@callback([
    Output("delete_project_modal", "is_open"),
    Output("delete_project_info_btn","n_clicks"),
    Output("delete_projects_dropdown","options")
    ], [Input("delete_project_info_btn", "n_clicks")]
)
def project_delete_modal(n_delete_info):
    if n_delete_info == 0:
        delete_project_modal_visible = False
        delete_projects_dropdown_options = []

    else:
        delete_project_modal_visible = True
        list_of_cards, project_names = extract_information_df(json_storage_file)
        delete_projects_dropdown_options = project_names
    
    n_delete_info = 0
    return delete_project_modal_visible, n_delete_info, delete_projects_dropdown_options

    
# Add Image and URL Link to Project Link Tables 
@callback(
    [# Add Image 
    Output("add_image_btn", "n_clicks"),
    Output("input_new_images_table", "data"),
    # Add Link
    Output("add_link_btn", "n_clicks"),
    Output("input_new_links_table", "data"),
    # Add Steps Taken
    Output("add_new_steps_taken", "n_clicks"),
    Output("input_new_steps_taken_table", "data"),
    # Add Steps ToDo
    Output("add_new_todo", "n_clicks"),
    Output("input_new_steps_todo_table", "data")
     ],[
        # Add Image Inputs
        Input("add_image_btn", "n_clicks"),
        State("input_new_image_link", "value"),
        State("input_new_images_table", "data"),
        # Add Link Inputs
        Input("add_link_btn", "n_clicks"),
        State("input_new_links", "value"),
        State("input_new_links_table", "data"),
        # Add Steps Taken Inputs
        Input("add_new_steps_taken", "n_clicks"),
        State("input_new_steps_taken", "value"),
        State("input_new_steps_taken_table", "data"),
        # Add Steps Todo Inputs
        Input("add_new_todo", "n_clicks"),
        State("input_new_steps_todo", "value"),
        State("input_new_steps_todo_table", "data")
    ]
)
def add_image_new_modal(n_image_link, image_link, image_df, n_link, links_value, links_df, n_steps_taken, input_step_taken, steps_taken_df, n_steps_todo, input_step_todo, steps_todo_df):
    
    if(n_image_link != 0):
        image_df = pd.DataFrame.from_dict(image_df)
        if image_link != '':  
            image_df = pd.concat([image_df, pd.DataFrame({'images': [image_link]})]) 
            image_df.reset_index()
        image_df.reset_index()
        image_table = image_df.to_dict('records')
        links_table = links_df
        steps_taken_table = steps_taken_df
        steps_todo_table = steps_todo_df
        n_image_link = 0 
        logging.info(f"Image link {image_link} added to new project")
        
    elif(n_link != 0):
        links_df = pd.DataFrame.from_dict(links_df)
        links_df = pd.concat([links_df, pd.DataFrame({'links': [links_value]})]) 
        links_df.reset_index()
        links_table = links_df.to_dict('records')
        image_table = image_df
        steps_taken_table = steps_taken_df
        steps_todo_table = steps_todo_df
        n_link = 0 
        logging.info(f"URL general link {links_value} added to new project")
        
        
    elif(n_steps_taken != 0):
        steps_taken_df = pd.DataFrame.from_dict(steps_taken_df)
        steps_taken_df = pd.concat([steps_taken_df, pd.DataFrame({'steps_taken': [input_step_taken]})]) 
        steps_taken_df.reset_index()
        steps_taken_table = steps_taken_df.to_dict('records')
        image_table = image_df 
        links_table = links_df
        steps_todo_table = steps_todo_df
        n_steps_taken = 0
        logging.info(f"Step taken {input_step_taken} added to new project")
        
    elif(n_steps_todo != 0):
        steps_todo_df = pd.DataFrame.from_dict(steps_todo_df)
        steps_todo_df = pd.concat([steps_todo_df, pd.DataFrame({'steps_todo': [input_step_todo]})]) 
        steps_todo_df.reset_index()
        steps_todo_table = steps_todo_df.to_dict('records')
        image_table = image_df 
        links_table = links_df
        steps_taken_table = steps_taken_df
        n_steps_todo = 0
        logging.info(f"Step to-do {input_step_todo} added to new project")
        
    else:
        image_table= image_df 
        links_table = links_df
        steps_taken_table = steps_taken_df
        steps_todo_table = steps_todo_df

    return n_image_link, image_table, n_link, links_table, n_steps_taken, steps_taken_table, n_steps_todo, steps_todo_table
   
   

