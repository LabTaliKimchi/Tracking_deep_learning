import yaml
"""create yaml file with the settings
    """

# Define the settings with several branches
General_settings= {
    'Create_sample_settings': {
        'Folder_with_data': 'F:/Juna/test',
        'video_file': 'f:/Juna/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT.avi',
        'list_frames': [1,100,530,640,2000],
        'number_first_movie':1
    },

}

# Write the settings to a YAML file
with open('General_settings.yaml', 'w') as file:
    yaml.dump(General_settings, file, default_flow_style=False)