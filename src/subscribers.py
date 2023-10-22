import os
import json
import logging


class Subscribers():
    def __init__(self, subscribers_file_path) -> None:
        self.subscribers_file_path = subscribers_file_path
        self.subscribers = self.load_from_file()
        logging.info(f"Subscribers: {len(self.subscribers)} from {self.subscribers_file_path}")
    def add_chat_id(self, chat_id):
        self.subscribers.add(chat_id)
        self.save_to_file()
    def get_all(self):
        return self.subscribers
    def load_from_file(self):
        if os.path.exists(self.subscribers_file_path):
            with open(self.subscribers_file_path, "r") as file:
                return set(json.load(file))
        else:
            return set()
    def save_to_file(self):
        with open(self.subscribers_file_path, "w") as file:
            json.dump(list(self.subscribers), file)