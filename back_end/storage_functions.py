import json
from os import path
from front_end.project_card import project_card
import pandas as pd
import logging


def convert_dataframe_to_cards(df):
    list_of_cards = []
    for index, row in df.iterrows():
        list_of_cards.append(project_card(row))
    return list_of_cards

def read_stored_information(path):
    projects_df = pd.read_json(path)
    return projects_df

def extract_information_df(path):
    try:
        projects_df = pd.read_json(path)
        list_of_cards = convert_dataframe_to_cards(projects_df)
        project_names = list(projects_df.get('name'))
    except:
        list_of_cards = []
        project_names = []
        
    return list_of_cards, project_names

def delete_project_with_name(path, project_name):
    project_df = read_stored_information(path)
    project_to_edit = project_df[project_df['name']== project_name].head()
    project_df = project_df.drop(project_to_edit.index[0])
    project_df.to_json(path)
        
        
def save_edited_project(json_storage_file, selected_project_to_edit,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, input_image_links_edit, input_links_edit, input_edit_steps_taken, input_edit_steps_todo):
        
        # save edited project details 
        project_df = read_stored_information(json_storage_file)
        # locate the row to update
        row_index = project_df.loc[project_df['name'] == selected_project_to_edit].index[0]
                
        # update the row with new values
        project_df.loc[row_index, 'name'] = input_project_name_edit
        project_df.loc[row_index, 'hobby'] = input_hobby_name_edit
        project_df.loc[row_index, 'notes'] = input_notes_edit
        project_df.loc[row_index, 'status'] = project_status_input_edit 
        project_df.loc[row_index, 'links'] = str(input_links_edit) # turn dictionary of image links into string to avoid errors       
        project_df.loc[row_index, 'images'] = str(input_image_links_edit) # turn dictionary of image links into string to avoid errors
        project_df.loc[row_index, 'steps_taken'] = str(input_edit_steps_taken) # turn dictionary of image links into string to avoid errors       
        project_df.loc[row_index, 'steps_todo'] = str(input_edit_steps_todo) # turn dictionary of image links into string to avoid errors

        logging.info(f"Edited project {selected_project_to_edit} saved. \n Project Info: {project_df.loc[project_df['name'] == selected_project_to_edit]}")
        
        # save dataframe to json
        project_df.to_json(json_storage_file)          
        
        # re load displayed cards
        list_of_cards, project_names = extract_information_df(json_storage_file)    
        
        return list_of_cards, project_names
