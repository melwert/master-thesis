from typing import Dict

from utils.dictionary_helper import DictionaryHelper


class BitbucketAnalyzer:

    def __init__(self) -> None:
        pass

    @staticmethod
    def analyze_pull_request(pull_request: Dict, activities: Dict) -> None:
        author = pull_request['author']['user']['displayName']

        declined_per_author = {}
        for activity in activities:
            if activity['action'] == 'DECLINED':
                DictionaryHelper.add_one_to_dict_counter(declined_per_author, author)

        return declined_per_author
