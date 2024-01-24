import uuid
import pandas as pd
import logging
from datetime import date

class Event:        
    def __init__(self, project_name, event_date, description, duration):
        self.id = str(uuid.uuid4())
        self.project_name = project_name,
        self.event_date = event_date,
        self.description = description,
        self.duration = duration
        
    def save_event(self,path_):
        try:
            # read existing dataframe from json file
            events_df = pd.read_json(path_)
            # add new project dataframe to existing dataframe 
            events_df = pd.concat([events_df, pd.DataFrame.from_dict(self.__dict__)], ignore_index=True)
        except:
            # # handle the exception
            #logging.debug(f"Exception occured: {error} \n New JSON file created.")
            events_df = pd.DataFrame(vars(self))

        # save combined dataframe in json
        events_df.to_json(path_)       