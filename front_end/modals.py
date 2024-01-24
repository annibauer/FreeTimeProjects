import dash_bootstrap_components as dbc
from dash import html, dcc
from storage.settings import project_status_array
from dash import dash_table
import pandas as pd

style_modals = {'padding':'30px'}
style_inner_modals = {'padding':'10px','margin':'20px'}
style_image_inputs = { 'height':'100%', 'align':'right'}
style_row_link_table = {'height':'100%'}
width_col_modal_label = 2
width_col_modal_inputs = 9
style_table_links = {"width": "100%", "height":"100%", "overflowX": "auto","background-color":"rgba(0,0,0,0.5)", "color":"black"}
style_inputs_url = {"width": "100%", 'margin-top':'20px', 'margin-bottom': '10px'}
style_inputs_general = {"width": "100%"}
style_input_notes = {"height": "200px", "width":"100%"}
style_header = {'display': 'none'}
style_dropdown = {'color':"black"}
style_date_picker = {'width':'100%', 'margin':'20px'}

new_project_modal_element =  html.Div([dbc.Modal(children=[
                dbc.ModalHeader(dbc.ModalTitle("New Project")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6('Project Name')
                        ],width=width_col_modal_label),
                        dbc.Col([
                            dcc.Input(id="input_new_project_name", type="text", placeholder="Enter Project Name", style=style_inputs_general)
                        ], width=width_col_modal_inputs)], style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H6('Hobby ')
                        ],width=width_col_modal_label),
                        dbc.Col([
                            dcc.Input(id="input_new_project_hobby", type="text", placeholder="Enter Hobby Name", style=style_inputs_general)
                        ], width=width_col_modal_inputs)],  style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H6('Notes ')
                        ],width=width_col_modal_label),
                        dbc.Col([                            
                            dcc.Textarea(
                                id='input_new_project_notes',
                                value='',
                                style={'width': '100%', 'height': 200},
                                placeholder="Enter Notes"
                            ),
                        ], width=width_col_modal_inputs)],  style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H6('Project Status')
                        ],width=width_col_modal_label),
                        dbc.Col([
                            dcc.Dropdown(project_status_array, project_status_array[0], id='dd_project_status', style=style_dropdown),
                        ], width=width_col_modal_inputs)],  style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H6('Links')
                            ],width=width_col_modal_label),
                        dbc.Col([
                            dbc.Row([
                                dash_table.DataTable(id='input_new_links_table', data=pd.DataFrame(columns=['links']).to_dict('records'), style_header=style_header, style_table=style_table_links,row_deletable=True, style_cell={'textAlign': 'left'}, style_as_list_view=True)
                                ], style = style_row_link_table),
                            dbc.Row([
                                dcc.Input(id="input_new_links", type="text", placeholder="Enter URL Link", style=style_inputs_url),
                            ]),
                            dbc.Row([
                                dbc.Button("Add URL", id="add_link_btn", className="me-1", n_clicks=0)
                                ]),
                        ], width=width_col_modal_inputs, style=style_image_inputs)
                        ], style=style_inner_modals),                    
                    dbc.Row([
                        dbc.Col([
                            html.H6('Images ')
                            ],width=width_col_modal_label),
                        dbc.Col([
                            dbc.Row([
                                dash_table.DataTable(id='input_new_images_table', data=pd.DataFrame().to_dict('records'), style_header=style_header, style_table=style_table_links,row_deletable=True, style_cell={'textAlign': 'left'}, style_as_list_view=True)
                                ], style = style_row_link_table),
                            dbc.Row([
                                dcc.Input(id="input_new_image_link", type="text", placeholder="Enter Image URL Link", style=style_inputs_url)
                            ]),
                            dbc.Row([
                                dbc.Button("Add image", id="add_image_btn", className="me-1", n_clicks=0)
                            ])
                        ], width=width_col_modal_inputs, style=style_image_inputs)
                        ], style=style_inner_modals),
                        dbc.Row([
                        dbc.Col([
                            html.H6('Steps Taken')
                            ],width=width_col_modal_label),
                        dbc.Col([
                            dbc.Row([
                                dash_table.DataTable(id='input_new_steps_taken_table', data=pd.DataFrame().to_dict('records'),style_header=style_header, style_table=style_table_links,row_deletable=True, style_cell={'textAlign': 'left'}, style_as_list_view=True)
                                ], style = style_row_link_table),
                            dbc.Row([
                                dcc.Input(id="input_new_steps_taken", type="text", placeholder="Enter Step Taken", style=style_inputs_url),
                            ]),
                            dbc.Row([
                                dbc.Button("Add Task", id="add_new_steps_taken", className="me-1", n_clicks=0)
                                ]),
                        ], width=width_col_modal_inputs, style=style_image_inputs)
                        ], style=style_inner_modals),                    
                    dbc.Row([
                        dbc.Col([
                            html.H6('To Do')
                            ],width=width_col_modal_label),
                        dbc.Col([
                            dbc.Row([
                                dash_table.DataTable(id='input_new_steps_todo_table', data=pd.DataFrame().to_dict('records'), style_header=style_header,style_table=style_table_links,row_deletable=True, style_cell={'textAlign': 'left'}, style_as_list_view=True)
                                ], style = style_row_link_table),
                            dbc.Row([
                                dcc.Input(id="input_new_steps_todo", type="text", placeholder="Enter To Do", style=style_inputs_url)
                            ]),
                            dbc.Row([
                                dbc.Button("Add Task", id="add_new_todo", className="me-1", n_clicks=0)
                            ])
                        ], width=width_col_modal_inputs, style=style_image_inputs)
                        ], style=style_inner_modals),
                    
                    dbc.Row([html.H6(id='project_save_status')],  style=style_inner_modals),
                    dbc.Row([dbc.Button("Add Project", id="add_project_btn", className="me-1", n_clicks=0)])],  style=style_inner_modals),

            ],
            id="new_project_modal",
            size="lg",
            is_open=False,
            style=style_modals
        )])


edit_project_modal_element =  html.Div([dbc.Modal(children=[
                dbc.ModalHeader(dbc.ModalTitle("Edit Project")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([html.H5("Select Project to Edit")]),
                        dbc.Col([dcc.Dropdown(id='edit_projects_dropdown', style=style_dropdown)
                        ])], style=style_inner_modals),
                    
                    dbc.Row([
                        dbc.Col([
                            html.H6('Project Name')
                        ]),
                        dbc.Col([
                            dcc.Input(id="input_edit_project_name", type="text", placeholder="Enter Project Name", style=style_inputs_general)
                        ])], style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H6('Hobby ')
                        ]),
                        dbc.Col([
                            dcc.Input(id="input_edit_project_hobby", type="text", placeholder="Enter Hobby Name", style=style_inputs_general)
                        ])], style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H6('Notes ')
                        ]),
                        dbc.Col([
                            dcc.Textarea(
                                id='input_edit_project_notes',
                                value='',
                                style={'width': '100%', 'height': 200},
                                placeholder="Enter Notes"
                            ),
                        ])], style=style_inner_modals),
                
                    dbc.Row([
                        dbc.Col([
                            html.H6('Project Status')
                        ]),
                        dbc.Col([
                            dcc.Dropdown(project_status_array, project_status_array[0], id='dd_project_status_edit', style=style_dropdown),
                        ])], style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H6('Links')
                            ],width=width_col_modal_label),
                        dbc.Col([
                            dbc.Row([
                                dash_table.DataTable(id='input_edit_links_table', data=pd.DataFrame().to_dict('records') , style_table=style_table_links,row_deletable=True, style_cell={'textAlign': 'left'}, style_as_list_view=True)
                                ],  style = style_row_link_table),
                            dbc.Row([
                                dcc.Input(id="input_edit_links", type="text", placeholder="Enter URL Link", style=style_inputs_url)
                            ]),
                            dbc.Row([
                                dbc.Button("Add URL", id="add_edit_link_btn", className="me-1", n_clicks=0)
                                ]),
                        ], width=width_col_modal_inputs, style=style_image_inputs)
                        ], style=style_inner_modals),                    
                    dbc.Row([
                        dbc.Col([
                            html.H6('Images ')
                            ],width=width_col_modal_label),
                        dbc.Col([
                            dbc.Row([
                                dash_table.DataTable(id='input_edit_images_table', data=pd.DataFrame().to_dict('records'),  style_table=style_table_links,row_deletable=True, style_cell={'textAlign': 'left'}, style_as_list_view=True)
                                ],  style = style_row_link_table),
                            dbc.Row([
                                dcc.Input(id="input_edit_image_link", type="text", placeholder="Enter Image URL Link", style=style_inputs_url)
                            ]),
                            dbc.Row([dbc.Button("Add Image", id="add_edit_image_btn", className="me-1", n_clicks=0)])
                        ], width=width_col_modal_inputs, style=style_image_inputs)
                        ], style=style_inner_modals),
                    
                    dbc.Row([
                        dbc.Col([
                            html.H6('Steps Taken')
                            ],width=width_col_modal_label),
                        dbc.Col([
                            dbc.Row([
                                dash_table.DataTable(id='input_edit_steps_taken_table', data=pd.DataFrame().to_dict('records'), style_table=style_table_links,row_deletable=True, style_cell={'textAlign': 'left'}, style_as_list_view=True)
                                ], style = style_row_link_table),
                            dbc.Row([
                                dcc.Input(id="input_edit_steps_taken", type="text", placeholder="Enter URL Link", style=style_inputs_url),
                            ]),
                            dbc.Row([
                                dbc.Button("Add Task", id="add_edit_steps_taken", className="me-1", n_clicks=0)
                                ]),
                        ], width=width_col_modal_inputs, style=style_image_inputs)
                        ], style=style_inner_modals),                    
                    dbc.Row([
                        dbc.Col([
                            html.H6('To Do')
                            ],width=width_col_modal_label),
                        dbc.Col([
                            dbc.Row([
                                dash_table.DataTable(id='input_edit_steps_todo_table', data=pd.DataFrame().to_dict('records'), style_table=style_table_links,row_deletable=True, style_cell={'textAlign': 'left'}, style_as_list_view=True)
                                ], style = style_row_link_table),
                            dbc.Row([
                                dcc.Input(id="input_edit_steps_todo", type="text", placeholder="Enter To Do", style=style_inputs_url)
                            ]),
                            dbc.Row([
                                dbc.Button("Add Task", id="add_edit_todo", className="me-1", n_clicks=0)
                            ])
                        ], width=width_col_modal_inputs, style=style_image_inputs)
                        ], style=style_inner_modals),
                    
                    
                    dbc.Row([]),
                    dbc.Row([html.H6(id='project_save_status_edit')], style=style_inner_modals),
                    dbc.Row([dbc.Button("Save Project", id="save_project_btn", className="me-1", n_clicks=0)], style=style_inner_modals)
                    ]),
                    
            ],
            id="edit_project_modal",
            size="lg",
            is_open=False,
            style=style_modals
        )])


delete_project_modal_element =  html.Div([dbc.Modal(children=[
                dbc.ModalHeader(dbc.ModalTitle("Delete Project")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([html.H5("Select Project to Delete")]),
                        dbc.Col([dcc.Dropdown(id='delete_projects_dropdown', style=style_dropdown)
                        ])], style=style_inner_modals),
    
                    dbc.Row([html.H6(id='project_delete_status')], style=style_inner_modals),
                    dbc.Row([dbc.Button("Delete Project", id="delete_project_btn", className="me-1", n_clicks=0)], style=style_inner_modals)
                    ]),        
            ],
            id="delete_project_modal",
            size="lg",
            is_open=False,
            style=style_modals
        )])


add_event_modal =  html.Div([dbc.Modal(children=[
                dbc.ModalHeader(dbc.ModalTitle("Add Event")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([html.H5("Select Project")]),
                        dbc.Col([dcc.Dropdown(id='select_event_projects_dropdown', style=style_dropdown)
                        ])], style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([html.H5("Select Date")]),
                        dbc.Col([
                            dcc.DatePickerSingle(
                                id='date-picker-add-event'
                            ),
                            html.Div(id='output_date_picker_add_event')
                            ]),
                        ], style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H5("Event Description")
                        ]),
                        dbc.Col([
                            dcc.Input(id='event_description', placeholder='Event Description', style=style_inputs_general)
                        ])
                        ],  style=style_inner_modals),
                    dbc.Row([
                        dbc.Col([
                            html.H5("Event Duration [hours]")
                        ]),
                        dbc.Col([dcc.Dropdown(id='hours_event_dropdown', style=style_dropdown)])
                        ], style=style_inner_modals),

                    dbc.Row([dbc.Button("Add Event", id="add_event_btn", n_clicks=0)], style=style_inner_modals)
                    ]),        
            ],
            id="modal_add_event",
            size="lg",
            is_open=False,
            style=style_modals
        )])