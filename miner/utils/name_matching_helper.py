from utils.file_loader import FileLoader

class NameMatchingHelper:

    def __init__(self, dictionary_filename: str) -> None:
        self.name_dict = FileLoader.load_json_file_as_dict(dictionary_filename)
        pass

    def find_name(self, other_name: str) -> str:
        for person in self.name_dict:

            if other_name in person["other_names"]:
                return person["name"]

        return other_name
