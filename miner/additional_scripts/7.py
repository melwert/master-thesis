from utils.dictionary_helper import DictionaryHelper
from db.mongo_wrapper import MongoWrapper


def __analyze_jira():
    prs_cursor = bitbucket_pull_requests_collection.find({"closed": True})

    declines_per_descr_key = {}

    for pr in prs_cursor:
        issue_key = pr["title"].split(':', 1)[0]
        issue_key = issue_key.split(" ", 1)[0]

        matching_issue = jira_issues_collection.find_one({"key": issue_key})

        if matching_issue:

            description = matching_issue["fields"]["description"]

            if description:

                dict_key = ""

                if "Ziel" in description or "Goal" in description:
                    dict_key += "Ziel"
                if "Implementation" in description or "Implementierung" in description or "Umsetzung" in description or  "Konzept" in description or "Concept" in description:
                    dict_key += "Implementierung"
                # if "Konzept" in description or "Concept" in description:
                #     dict_key += "Concept"

                declines = 0

                decline_cursor = bitbucket_pull_request_changes_collection.find({"action": "DECLINED", "pr_name": pr["id"], "repo_slug": pr["repo_slug"]})

                for _ in decline_cursor:
                    declines += 1

                DictionaryHelper.append_value_to_dict_list(declines_per_descr_key, dict_key, declines)


    metrics = {}

    for category in declines_per_descr_key:
        metrics[category] = list(map(lambda element: {element: declines_per_descr_key[category].count(element)}, set(declines_per_descr_key[category])))

    print(metrics)



if __name__ == "__main__":

    mongo_wrapper = MongoWrapper("", "", "mongodb://localhost:27017")
    pi_database = mongo_wrapper.get_database("project_insight")

    bitbucket_pull_requests_collection = pi_database["bitbucket_pull_requests"]
    bitbucket_pull_request_activities_collection = pi_database["bitbucket_pull_request_activities"]
    bitbucket_pull_request_changes_collection = pi_database["bitbucket_pull_request_activities"]
    jira_issues_collection = pi_database["jira_issues"]
    jira_issue_histories_collection = pi_database["jira_issue_histories"]

    qa_loops_collection = pi_database["bitbucket_qa_loops"]

    __analyze_jira()

