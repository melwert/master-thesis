import os
from re import M
import statistics
from time import time
from typing import List, OrderedDict
from analyzing.bitbucket_analyzer import BitbucketAnalyzer
from mining.bitbucket_miner import BitbucketMiner
from mining.repo_miner import RepoMiner
from models.appsettings import Appsettings
from models.project import Project
from models.project_from_file import ProjectFromFile
from project_manager import ProjectManager
from utils.dictionary_helper import DictionaryHelper
from utils.file_loader import FileLoader
from db.mongo_wrapper import MongoWrapper
import numpy as np


def __analyze_bitbucket():

    # activities_cursor = bitbucket_pull_request_activities_collection.find({"action": "DECLINED", "repo_slug": "abc"})

    # x = 0

    # # declined_prs_by_author = {}
    # # prs_by_author = {}

    # for activity in activities_cursor:
    #     x +=1

    # print(x)

    #     pr_cursor = bitbucket_pull_requests_collection.find({"repo_slug": activity["repo_slug"], "id": activity["pr_name"]})

    #     for pr in pr_cursor:
    #          DictionaryHelper.add_one_to_dict_counter(declined_prs_by_author, pr["author"]["user"]["displayName"])

    # print(declined_prs_by_author)

    # pr_cursor = bitbucket_pull_requests_collection.find()

    # for pr in pr_cursor:
    #          DictionaryHelper.add_one_to_dict_counter(prs_by_author, pr["author"]["user"]["displayName"])

    # print(prs_by_author)

    pr_cursor = bitbucket_pull_requests_collection.find({"closed": True})

    prs_projects = {}
    prs_declined_gesamt = {}
    boxplot_values = {}

    for pr in pr_cursor:
        DictionaryHelper.append_value_to_dict_list(prs_projects, pr['repo_slug'], pr)

    for project in prs_projects:

        prs_authors = {}
        prs_authors_longer_than_a_year = {}
        pr_declined_pro_monat_dabei = {}

        for pr in prs_projects[project]:
            DictionaryHelper.append_value_to_dict_list(prs_authors, pr['author']['user']['displayName'], pr)

        for author in prs_authors:
            timestamps = []

            for pr in prs_authors[author]:
                timestamps.append(pr["createdDate"])

            #if max(timestamps) - min(timestamps) > 31536000000:
            if max(timestamps) - min(timestamps) > 0:
                prs_authors_longer_than_a_year[author] = prs_authors[author]

        #print(prs_authors_longer_than_a_year)

        for author in prs_authors_longer_than_a_year:
            timestamps = []

            for pr in prs_authors_longer_than_a_year[author]:
                timestamps.append(pr["createdDate"])

            earliest_pr = min(timestamps)
            latest_pr = max(timestamps)

            for pr in prs_authors_longer_than_a_year[author]:
                declined_count = 0
                
                declined_cursor = bitbucket_pull_request_activities_collection.find({"repo_slug": project, "action": "DECLINED", "pr_name": pr['id']})

                for _ in declined_cursor:
                    declined_count += 1

                monat_dabei = int((pr["createdDate"] - earliest_pr) / 2678400000)

                DictionaryHelper.append_value_to_dict_list(pr_declined_pro_monat_dabei, monat_dabei, declined_count)

        for month in pr_declined_pro_monat_dabei:
            DictionaryHelper.extend_value_to_dict_list(prs_declined_gesamt, month, pr_declined_pro_monat_dabei[month])
    
    #print(prs_declined_gesamt)

    month_metrics = {}

    for month in prs_declined_gesamt:
        month_metrics[month] = list(map(lambda element: {element: prs_declined_gesamt[month].count(element)}, set(prs_declined_gesamt[month])))

    print(month_metrics)

    # for month in prs_declined_gesamt:
    #     median = np.median(prs_declined_gesamt[month])
    #     lower_quartile = np.percentile(prs_declined_gesamt[month], 25)
    #     upper_quartile = np.percentile(prs_declined_gesamt[month], 75)
    #     x = prs_declined_gesamt[month]

    #     boxplot_month = {
    #         "count": len(prs_declined_gesamt[month]),
    #         "lower_whisker": min(prs_declined_gesamt[month]),
    #         "lower_quartile": lower_quartile,
    #         "median": median,
    #         "upper_quartile": upper_quartile,
    #         "upper_whisker": max(prs_declined_gesamt[month]),
    #     }

    #     boxplot_values[month] = boxplot_month

    # ordered_dict = OrderedDict(sorted(boxplot_values.items()))
    #print(ordered_dict)


if __name__ == "__main__":

    mongo_wrapper = MongoWrapper("", "", "mongodb://localhost:27017")
    pi_database = mongo_wrapper.get_database("project_insight")

    bitbucket_pull_requests_collection = pi_database["bitbucket_pull_requests"]
    bitbucket_pull_request_activities_collection = pi_database["bitbucket_pull_request_activities"]
    bitbucket_pull_request_changes_collection = pi_database["bitbucket_pull_request_activities"]
    jira_issues_collection = pi_database["jira_issues"]
    jira_issue_histories_collection = pi_database["jira_issue_histories"]

    qa_loops_collection = pi_database["bitbucket_qa_loops"]

    __analyze_bitbucket()

