from copy import deepcopy
import os
import shutil
import statistics
from typing import Dict, List, Tuple
from git import Repo
import numpy as np

from utils.dictionary_helper import DictionaryHelper


class RepoMiner:

    def __init__(self, working_dir: str) -> None:
        self.working_dir = working_dir

        os.chdir(self.working_dir)

    def checkout_repository(self, repo_path: str) -> str:
        repo_name = repo_path.rsplit("/", 1)[1]

        os.popen(f"git clone {repo_path}").read()

        return repo_name

    def get_file_infos(self, repo_path: str, folder_depth: int) -> Tuple[int, Dict]:
        file_count_per_directory = {}
        file_count = 0

        for root, dirs, files in os.walk(repo_path):

            if os.sep in root:
                relative_root_elements = root.split(os.sep)
                relative_root_elements.pop(0)
                relative_root_elements = relative_root_elements[0:folder_depth]

                relative_root = os.path.join(*relative_root_elements)
            else:
                relative_root = os.sep

            if os.sep in relative_root:
                pass

            for f in files:
                DictionaryHelper.add_one_to_dict_counter(file_count_per_directory, relative_root)
                file_count += 1
        
        return file_count, file_count_per_directory

    def remove_repository(self, repo_name: str):
        shutil.rmtree(repo_name, True)

    def get_changes(self, repo_name:str, branch_name: str, folder_depth: int) -> Dict:
        repo = Repo(f"{self.working_dir}/{repo_name}")
        assert not repo.bare

        all_commits = list(repo.iter_commits())

        file_changes_per_area = {}
        file_changes_per_dev = {}
        file_changes_per_area_and_dev = {}
        commit_message_lengths_per_area = {}
        commit_message_lengths_per_dev = {}
        commit_message_lengths_per_area_and_dev = {}
        commit_hours_template = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0, }
        commit_weekdays_template = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, }

        commit_hours = deepcopy(commit_hours_template)
        commit_weekdays = deepcopy(commit_weekdays_template)

        commit_hours_per_author = {}
        commit_weekdays_per_author = {}

        persons = {}

        commit_count = len(all_commits)

        for commit in all_commits:

            if not commit.author.name in persons:
                persons[commit.author.name] = {}

            DictionaryHelper.add_one_to_dict_counter(persons[commit.author.name], "commit_count")

            if commit.author.name not in commit_hours_per_author:
                commit_hours_per_author[commit.author.name] = deepcopy(commit_hours_template)

            if commit.author.name not in commit_weekdays_per_author:
                commit_weekdays_per_author[commit.author.name] = deepcopy(commit_weekdays_template)

            DictionaryHelper.add_one_to_dict_counter(commit_hours_per_author[commit.author.name], str(commit.authored_datetime.hour))
            DictionaryHelper.add_one_to_dict_counter(commit_weekdays_per_author[commit.author.name], str(commit.authored_datetime.weekday()))

            DictionaryHelper.add_one_to_dict_counter(commit_hours, str(commit.authored_datetime.hour))
            DictionaryHelper.add_one_to_dict_counter(commit_weekdays, str(commit.authored_datetime.weekday()))

            files = commit.stats.files.keys()

            for file in files:

                if "=>" in file:
                    # folder = file.split(" => ")[1]
                    # folder = folder.replace("}", "")

                    # if "/" in folder:
                    #     folder = folder.split("/", folder_depth)[0]
                    # else:
                    #     folder = "/"
                    # TODO Erkennung für Verschiebungen
                    pass
                else:
                    if "/" in file:
                        folder = file.split("/", folder_depth)[0]
                    else:
                        folder = "/"

                if not folder == ".github" and "." in folder:
                    pass

                DictionaryHelper.add_one_to_dict_counter(file_changes_per_area, folder)
                DictionaryHelper.append_value_to_dict_list(commit_message_lengths_per_area, folder, len(commit.message))

                DictionaryHelper.add_one_to_dict_counter(file_changes_per_dev, commit.author.name)
                DictionaryHelper.append_value_to_dict_list(commit_message_lengths_per_dev, commit.author.name, len(commit.message))

                if not folder in file_changes_per_area_and_dev:
                    file_changes_per_area_and_dev[folder] = {}
                
                if not folder in commit_message_lengths_per_area_and_dev:
                    commit_message_lengths_per_area_and_dev[folder] = {}

                DictionaryHelper.add_one_to_dict_counter(file_changes_per_area_and_dev[folder], commit.author.name)
                DictionaryHelper.append_value_to_dict_list(commit_message_lengths_per_area_and_dev[folder], commit.author.name, len(commit.message))

        for folder_name in commit_message_lengths_per_area_and_dev:
            for author in commit_message_lengths_per_area_and_dev[folder_name]:
                commit_message_lengths = commit_message_lengths_per_area_and_dev[folder_name][author]

                commit_message_lengths_per_area_and_dev[folder_name][author] = sum(commit_message_lengths) / len(commit_message_lengths)

        commit_message_lengths_per_area = self.__calculate_box_plot_parameters(commit_message_lengths_per_area)
        commit_message_lengths_per_dev = self.__calculate_box_plot_parameters(commit_message_lengths_per_dev)

        return \
            file_changes_per_area, \
            file_changes_per_dev, \
            file_changes_per_area_and_dev, \
            commit_message_lengths_per_area, \
            commit_message_lengths_per_dev, \
            commit_message_lengths_per_area_and_dev, \
            commit_hours, \
            commit_weekdays, \
            commit_hours_per_author, \
            commit_weekdays_per_author, \
            persons, \
            commit_count

    @staticmethod
    def __calculate_box_plot_parameters(data: Dict):

        for key in data:

            min_value = min(data[key])
            q1 = np.quantile(data[key], .25)
            median = statistics.median(data[key])
            q3 = np.quantile(data[key], .75)
            max_value = max(data[key])

            data[key] = [min_value, q1, median, q3, max_value]
 
        return data