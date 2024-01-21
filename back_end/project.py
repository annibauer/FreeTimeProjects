import uuid
import json
import os
from os import path
import pandas as pd
import logging 

class Project:
    
    def __init__(self, name, hobby, status, notes, steps_taken, next_steps, links, images):
        self.id = str(uuid.uuid4())
        self.hobby = hobby,
        self.name = name,
        self.status = status,
        self.notes = notes,
        self.steps_taken = steps_taken,
        self.steps_todo = next_steps,
        self.links = links,
        self.images = images
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
    def save_project(self, path_): 
        try:
            # read existing dataframe from json file
            projects_df = pd.read_json(path_)
            # add new project dataframe to existing dataframe 
            self.images = [self.images]  
            projects_df = pd.concat([projects_df, pd.DataFrame.from_dict(self.__dict__)], ignore_index=True)
 
        except Exception as error:
            # handle the exception
            logging.debug(f"Exception occured: {error} \n New JSON file created.")
            projects_df = pd.DataFrame(vars(self))

        
        # save combined dataframe in json
        projects_df.to_json(path_)       
    