from typing import OrderedDict
from utils.dictionary_helper import DictionaryHelper
from db.mongo_wrapper import MongoWrapper

def __analyze_bitbucket():
    pr_cursor = bitbucket_pull_requests_collection.find()

    prs_by_author = {}

    for pr in pr_cursor:
        DictionaryHelper.add_value_to_dict_counter(prs_by_author, pr["repo_slug"], pr["properties"]["resolvedTaskCount"])
        DictionaryHelper.add_value_to_dict_counter(prs_by_author, pr["repo_slug"], pr["properties"]["openTaskCount"])

    ordered_dict = OrderedDict(sorted(prs_by_author.items()))

    print(dict(ordered_dict))


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

