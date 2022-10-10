
from numbers import Number
from typing import Dict
from utils.file_loader import FileLoader
from utils.dictionary_helper import DictionaryHelper
from utils.name_matching_helper import NameMatchingHelper


class CommitCountToNamespaceMapper:

    def map_commit_counts_to_namespaces(data: Dict) -> Dict:

        mapped_data = {}

        for key in data:

            csharp_namespace = data[key]["csharp_namespace"]
            DictionaryHelper.initialize_dict_if_not_existing(mapped_data, csharp_namespace)

            contributors: Number = data[key]["contributors"]

            for contributor in contributors:
                #contributor["commiter"] = NameMatchingHelper.find_name(contributor["commiter"])

                DictionaryHelper.add_value_to_dict_counter(mapped_data[csharp_namespace], contributor["commiter"], int(contributor["commit_count"]))

        return mapped_data
