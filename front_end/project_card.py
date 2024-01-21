import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd
from back_end.data_processing import transform_stored_data_links, transform_stored_data_links_url, transform_stored_data_carousel
from storage.settings import project_status_array, project_status_color_array


style_carousel = {'width': 'auto', 'justify':'center', 'margin':'10px'}
style_row = {'justify':'center'}
style_table_div= {'margin':'10px'}
style_table ={"width": "100%", "overflowX": "auto", "background-color":"rgba(0,0,0,0)", "color":"black"}
style_title_info = {'margin':'0px'}
style_header = {'fontWeight': 'bold', 'textAlign': 'center'}
style_cell = {'textAlign': 'left'}

def project_card(project): 
    links_table_df = transform_stored_data_links_url(project["links"])
    image_carousel_items = transform_stored_data_carousel(project["images"])
    steps_taken_df = transform_stored_data_links(project["steps_taken"])
    steps_todo_df = transform_stored_data_links(project["steps_todo"])
    
    # change footer color based on project status
    index_project_status = project_status_array.index(project["status"])
    background_color_project_status = project_status_color_array[index_project_status]
    style_footer = {'background-color': str(background_color_project_status)}
    

    card = dbc.Col([dbc.Card(id= str(project["id"]), children=[
            dbc.CardHeader(project["hobby"]),
            dbc.CardBody(
                [
                    dbc.Row([html.H4(project["name"], className="card-title"),]),
                    dbc.Row([dbc.Carousel(
                            items=image_carousel_items,
                            controls=True,
                            indicators=True,
                            interval=3000
                        )],style=style_carousel),
                    dbc.Row([dash_table.DataTable(links_table_df.to_dict('records'), style_header=style_header ,style_table=style_table, style_cell=style_cell)], style=style_table_div),
                    dbc.Row([dash_table.DataTable(steps_taken_df.to_dict('records'),style_header=style_header, style_table=style_table, style_cell=style_cell)], style=style_table_div),
                    dbc.Row([dash_table.DataTable(steps_todo_df.to_dict('records'), style_header=style_header, style_table=style_table, style_cell=style_cell)], style=style_table_div),
                    dbc.Row([html.P(project["notes"], className="card-text")]),
                ]
            ),
            dbc.CardFooter(project["status"], style=style_footer),
        ], style={"font-size": "70%", "margin":"10px" },
    )], width=6)
        
    return card