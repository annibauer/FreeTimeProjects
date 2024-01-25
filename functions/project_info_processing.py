from functions.project import Project
import logging
import pandas as pd
from functions.storage_functions import read_stored_information, extract_information_df
from functions.data_processing import transform_stored_data_links
from functions.event import Event

def add_new_project(json_storage_file, input_project_name, input_hobby_name, project_status_input, input_notes, input_steps_taken, input_steps_todo, input_links, input_image_links):
    logging.info("Project save trigger button pressed")
    # create and save new project
    new_project = Project(input_project_name, input_hobby_name, project_status_input, input_notes, str(input_steps_taken), str(input_steps_todo), str(input_links), str(input_image_links))
    new_project.save_project(json_storage_file)
    project_save_status = 'Project: '+ str(input_project_name) + ' saved.'
    
    logging.info(f' New project {input_project_name} added')
    # read saved project data to display
    list_of_cards, project_names, project_ids = extract_information_df(json_storage_file)
    # reset add new project button
    n_new = 0
    # clear input fields 
    input_project_name, input_hobby_name, input_notes, project_status_input = '','','',''
    
    return list_of_cards, project_names, n_new, project_save_status, input_project_name, input_hobby_name, input_notes, project_status_input

# delete project 
def delete_project_with_name(path, project_name):
    logging.info(f'Project delete intitiated: {project_name}')
    project_df = read_stored_information(path)
    project_to_edit = project_df[project_df['name']== project_name].head()
    print(project_to_edit)
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
        list_of_cards, project_names, project_ids = extract_information_df(json_storage_file)
        
        return list_of_cards, project_names

def load_data_into_modal(json_storage_file,selected_project_to_edit):
    logging.info(f"Project to edit opened: {selected_project_to_edit}")
    # load selected project
    project_df = read_stored_information(json_storage_file)
    project_to_edit= project_df[project_df['name']== selected_project_to_edit]
    
    # load saved data from selected project into inputs
    input_edit_project_name = project_to_edit['name'].values[:1][0]
    input_edit_project_hobby = project_to_edit['hobby'].values[:1][0]
    input_edit_project_notes = project_to_edit['notes'].values[:1][0]
    dd_project_status_edit = project_to_edit['status'].values[:1][0]
    dict_images = project_to_edit['images'].values[:1][0]
    dict_links = project_to_edit['links'].values[:1][0]
    dict_steps_taken = project_to_edit['steps_taken'].values[:1][0]
    dict_steps_todo = project_to_edit['steps_todo'].values[:1][0]
    # transform string of dict into dict for dashtable
    image_links_edit = transform_stored_data_links(dict_images).to_dict('records')
    links_edit = transform_stored_data_links(dict_links).to_dict('records')
    steps_taken_edit = transform_stored_data_links(dict_steps_taken).to_dict('records')
    steps_todo_edit = transform_stored_data_links(dict_steps_todo).to_dict('records')
    
    return input_edit_project_name, input_edit_project_hobby, input_edit_project_notes, dd_project_status_edit, image_links_edit, links_edit, steps_taken_edit, steps_todo_edit

def add_image_to_new_project(json_storage_file,  selected_project_to_edit, image_link, input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, input_image_links_edit, input_links_edit, input_steps_taken_edit, input_steps_todo_edit):
    input_image_links_edit = pd.DataFrame.from_dict(input_image_links_edit)
    input_image_links_edit = pd.concat([input_image_links_edit, pd.DataFrame({'images': [image_link]})]) 
    input_image_links_edit.reset_index()
    image_links_edit = input_image_links_edit.to_dict('records')
    list_of_cards, project_names  = save_edited_project(json_storage_file, selected_project_to_edit,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, input_links_edit, input_steps_taken_edit, input_steps_todo_edit)
    n_image_edit = 0 
    logging.info(f"Image link added {image_link} to project {selected_project_to_edit}")
    image_link = ''
    return list_of_cards, n_image_edit, image_links_edit, image_link
    
def add_general_link_to_new_project(json_storage_file, selected_project_to_edit, url_link, input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, input_links_edit, steps_taken_edit, steps_todo_edit):
    input_links_edit = pd.DataFrame.from_dict(input_links_edit)
    input_links_edit = pd.concat([input_links_edit, pd.DataFrame({'links': [url_link]})]) 
    input_links_edit.reset_index()
    links_edit = input_links_edit.to_dict('records')
    list_of_cards, project_names  = save_edited_project(json_storage_file, selected_project_to_edit,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, links_edit, steps_taken_edit, steps_todo_edit)
    # reset button    
    n_links_edit = 0
    logging.info(f"General URL link added {url_link} to project {selected_project_to_edit}")
    url_link = ''
    return list_of_cards, n_links_edit,links_edit, url_link
    
def add_steps_taken_to_new_project(json_storage_file, selected_project_to_edit, input_step_taken ,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, links_edit,steps_todo_edit):
    input_steps_taken_edit = pd.DataFrame.from_dict(input_steps_taken_edit)
    input_steps_taken_edit = pd.concat([input_steps_taken_edit, pd.DataFrame({'steps_taken': [input_step_taken]})]) 
    input_steps_taken_edit.reset_index()
    steps_taken_edit = input_steps_taken_edit.to_dict('records')
    list_of_cards, project_names  = save_edited_project(json_storage_file, selected_project_to_edit,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, links_edit, steps_taken_edit, steps_todo_edit)
    # reset button    
    n_steps_taken_edit = 0
    logging.info(f"Step taken {input_step_taken} added to project {selected_project_to_edit}")
    input_step_taken = ''
    return list_of_cards, n_steps_taken_edit, steps_taken_edit, input_step_taken
    
def add_steps_todo_to_new_project(json_storage_file, selected_project_to_edit, input_step_todo, input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, links_edit, steps_taken_edit, steps_todo_edit):
    input_steps_todo_edit = pd.DataFrame.from_dict(input_steps_todo_edit)
    input_steps_todo_edit = pd.concat([input_steps_todo_edit, pd.DataFrame({'steps_todo': [input_step_todo]})]) 
    input_steps_todo_edit.reset_index()
    steps_todo_edit = input_steps_todo_edit.to_dict('records')
    list_of_cards, project_names  = save_edited_project(json_storage_file, selected_project_to_edit,input_project_name_edit,input_hobby_name_edit,input_notes_edit, project_status_input_edit, image_links_edit, links_edit, steps_taken_edit, steps_todo_edit)
    # reset button    
    n_steps_todo_edit = 0
    logging.info(f"To-do {input_step_todo} added to project {selected_project_to_edit}")
    
    return list_of_cards, n_steps_todo_edit, steps_todo_edit, input_step_todo

def add_new_event(json_storage_file, json_events_file, project_name_event,date_value, event_descrption, hours_event):
    new_event = Event(project_name_event, date_value, event_descrption, hours_event)
    new_event.save_event(json_events_file)
    
    project_df = read_stored_information(json_storage_file)    
    row_index = project_df.loc[project_df['name'] == project_name_event].index[0]
    steps_taken_str_obj = project_df.loc[row_index, 'steps_taken'] 
    if(steps_taken_str_obj != '[]'):
        comma = ', '
    else:
        comma = ''
    new_steps_taken = steps_taken_str_obj[0:len(steps_taken_str_obj)-1] + comma + str({'steps_taken': str(event_descrption)}) + "]"
    project_df.loc[row_index, 'steps_taken'] = new_steps_taken
    project_df.to_json(json_storage_file)   
    