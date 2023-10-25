import os

class MessagesBuilder():
    def __init__(self, data_folder_path):
        self.data_folder_path = data_folder_path

    def _read_text_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as tehilim_file:
            tehilim_message = tehilim_file.read()
        return tehilim_message

    def get_tehilim_message(self):
        tehilim_message = self._read_text_from_file(os.path.join(self.data_folder_path, "tehilim_message.txt"))
        return tehilim_message

    def get_oref_message(self):
        oref_message = self._read_text_from_file(os.path.join(self.data_folder_path, "oref_message.txt"))
        return oref_message
