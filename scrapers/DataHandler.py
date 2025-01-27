import os
import pandas as pd
import json
import logging

class DataHandler:
    def save_to_csv(self, data, file_path, columns=None):
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(file_path, index=False, encoding='utf-8')
        logging.info(f"Data saved to '{file_path}'.")

    def save_to_json(self, data, file_path):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Data saved to JSON at '{file_path}'.")

    def load_csv(self, file_path):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            return df
        else:
            logging.error(f"CSV file not found: {file_path}")
            return None

    def load_json(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)
        else:
            logging.error(f"JSON file not found: {file_path}")
            return None