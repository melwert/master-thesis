from numbers import Number
from typing import Dict, List, Tuple


class DictionaryHelper:

# based on BachelorThesisProject

    def __init__(self):
        pass

    @staticmethod
    def add_one_to_dict_counter(dictionary: Dict, value_name: str):
        if not dictionary.get(value_name) == None:
            dictionary[value_name] += 1
        else:
            dictionary[value_name] = 1

    @staticmethod
    def add_value_to_dict_counter(dictionary: Dict, value_name: str, value: Number):
        if not dictionary.get(value_name) == None:
            dictionary[value_name] += value
        else:
            dictionary[value_name] = value

    @staticmethod
    def initialize_dict_if_not_existing(dictionary: Dict, value_name: str):
        if not value_name in dictionary:
            dictionary[value_name] = {}

    @staticmethod
    def join_matching_number_dicts(first_dict: Dict, second_dict: Dict):
        for entry in second_dict:
            first_dict[entry] += second_dict[entry]

        return first_dict

    @staticmethod
    def dict_to_lists(data: Dict) -> Tuple[List, List]:
        values = []
        keys = []
        
        for key in data:
            keys.append(key)
            values.append(data[key])

        return values, keys

    @staticmethod
    def put_into_new_key_below_threshold(data: Dict, new_key: str, threshold: float | int) -> Dict:
        new_data = {}

        for key in data:
            if data[key] < threshold:
                DictionaryHelper.add_value_to_dict_counter(new_data, new_key, data[key])
            else:
                new_data[key] = data[key]

        return new_data

    @staticmethod
    def two_d_dict_to_lists(data: Dict) -> Tuple[List[List], List, List]:
        column_keys = DictionaryHelper.__get_all_column_keys_sorted(data)

        rows = []

        for dict_row in data:
            row = [0] * len(column_keys)
            
            for dict_column in data[dict_row]:
                
                if dict_column in column_keys:
                    key_index = column_keys.index(dict_column)
                    
                    row[key_index] = data[dict_row][dict_column]

            rows.append(row)

        row_labels = list(data.keys())

        return rows, row_labels, column_keys        

    @staticmethod
    def append_value_to_dict_list(dictionary: Dict, value_name: str, value: any):
        if dictionary.get(value_name) == None:
            dictionary[value_name] = [value]
        else:
            dictionary[value_name].append(value)


    @staticmethod
    def __get_all_column_keys_sorted(data: Dict) -> List:
        column_keys = []

        for row in data:
            for key in data[row]:

                if not key in column_keys:
                    column_keys.append(key)

        return sorted(column_keys)
