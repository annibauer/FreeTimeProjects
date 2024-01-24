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

def read_stored_events_information(path):
    try:
        events_df = pd.read_json(path)
    except:
        events_df = pd.DataFrame()
        events_df.to_json(path)     
    
    return events_df
