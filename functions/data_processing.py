import json
import pandas as pd
from dash import dcc

# transform stored strings of dict variables within saved dataframe back into dictionaries and transformed to 
def transform_stored_data_links(dict_images):
    json_acceptable_string = dict_images.replace("'", "\"")
    d = json.loads(json_acceptable_string)          
    data_table = pd.DataFrame(data=d)
    return data_table

def transform_stored_data_links_url(dict_links):
    json_acceptable_string = dict_links.replace("'", "\"")
    d = json.loads(json_acceptable_string)          
    data_table = pd.DataFrame(data=d)
    return data_table

def transform_stored_data_carousel(dict_images):
    json_acceptable_string = dict_images.replace("'", "\"")
    dict_images = json.loads(json_acceptable_string)      
    items = []
    key = 1
    for image in dict_images:
        item = {"key":str(key), "src":str(image["images"]), "img_style":{"object-fit":"contain","height":"300px" }}
        items.append(item)
        key = key+1 
        
    return items
