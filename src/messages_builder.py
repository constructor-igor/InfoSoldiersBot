import os
import json
from datetime import datetime
import logging


class MessagesBuilder():
    def __init__(self, data_folder_path):
        self.data_folder_path = data_folder_path

    def _read_text_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as tehilim_file:
            tehilim_message = tehilim_file.read()
        return tehilim_message

    def get_message(self, file_path):
        message = self._read_text_from_file(os.path.join(self.data_folder_path, file_path))
        return message

    def get_tehilim_message(self):
        tehilim_message = self._read_text_from_file(os.path.join(self.data_folder_path, "tehilim_message.txt"))
        return tehilim_message

    def get_oref_message(self):
        oref_message = self._read_text_from_file(os.path.join(self.data_folder_path, "oref_message.txt"))
        return oref_message

    def get_truma_message(self):
        truma_message = self._read_text_from_file(os.path.join(self.data_folder_path, "truma_message.txt"))
        return truma_message

    def _read_json_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    def import_scheduler(self):
        all_items = []
        json_file_path = os.path.join(self.data_folder_path, "messages_scheduler_config.json")
        try:
            data = self._read_json_file(json_file_path)
            for entry in data:
                time_string = entry['time']
                file_name = entry['file_name']
                parsed_time = datetime.strptime(time_string, "%H:%M")
                hours = parsed_time.hour
                minutes = parsed_time.minute
                logging.info(f"Time: {hours:02d}:{minutes:02d}, File Name: {file_name}")
                all_items.append((hours, minutes, file_name))
            return all_items
        except FileNotFoundError:
            logging.error(f"Error: File '{json_file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{json_file_path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
