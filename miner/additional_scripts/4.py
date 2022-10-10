from utils.dictionary_helper import DictionaryHelper
from db.mongo_wrapper import MongoWrapper
import numpy as np


def __analyze_bitbucket():

    pr_cursor = bitbucket_pull_requests_collection.find({"closed": True})

    prs_projects = {}
    prs_declined_gesamt = {}
    boxplot_values = {}

    declined_per_proj = {}

    for pr in pr_cursor:
        DictionaryHelper.append_value_to_dict_list(prs_projects, pr['repo_slug'], pr)

    for project in prs_projects:

        prs_authors = {}
        prs_authors_longer_than_a_year = {}
        pr_declined_pro_monat_dabei = {}

        for pr in prs_projects[project]:
            declined_count = 0
                
            declined_cursor = bitbucket_pull_request_activities_collection.find({"repo_slug": project, "action": "DECLINED", "pr_name": pr['id']})

            for _ in declined_cursor:
                declined_count += 1

            DictionaryHelper.append_value_to_dict_list(declined_per_proj, project, declined_count)

    month_metrics = {}

    for month in declined_per_proj:
        month_metrics[month] = list(map(lambda element: {element: declined_per_proj[month].count(element)}, set(declined_per_proj[month])))

    print(month_metrics)


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

