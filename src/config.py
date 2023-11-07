import os
import json


class Config():
    def __init__(self):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        # Access the values from the configuration dictionary
        self.bot_api_token = config['Credentials']['bot_api_token']
        self.bot_name = config['Credentials']['bot_name']
        self.chat_id = config['Credentials']['chat_id']
        self.log_folder_path = config['Paths']['log_folder_path']
        self.subscribers_file_path = config['Paths']['subscribers_file_path']
        self.data_folder_path = config['Paths']['data_folder_path']
        self.kidnapped_person_file_path = os.path.join(self.data_folder_path, "Bring them home November 6 English.pdf")


configuration = Config()
