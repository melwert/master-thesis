import csv
import json
from os import walk
from typing import Generic, List, TypeVar

T = TypeVar('T')
class FileLoader:

    def __init__(self):
        pass

    @staticmethod
    def load_json_list_as_class_instance_list(path: str, type: Generic[T]) -> List[T]:
        with open(path) as json_file:
            data = json_file.read()
            data_dict = json.loads(data)

            instances = []
            for entry in data_dict:
                instance = type(entry)
                instances.append(instance)
        return instances

    @staticmethod
    def load_json_file_as_dict(path: str):
        with open(path) as json_file:
            data = json_file.read()
            data_dict = json.loads(data)
        return data_dict

    @staticmethod
    def load_file_as_string(path: str):
        with open(path) as json_file:
            data = json_file.read()
        return data

    @staticmethod
    def load_file_as_csv(folder_path: str, filename: str):
        with open(f"{folder_path}/{filename}") as csv_file:
            file_content = csv.reader(csv_file, delimiter = ",", quotechar = "|")
            return file_content

    @staticmethod
    def get_filenames(save_path: str):
        (_, _, filenames) = next(walk(save_path))
        return filenames

    @staticmethod
    def get_filenames_with_type_filter(folder_path: str, type: str):
        (_, _, filenames) = next(walk(folder_path))
        json_filenames = [filename for filename in filenames if type in filename]
        return json_filenames
