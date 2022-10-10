from datetime import datetime, timezone
from utils.dictionary_helper import DictionaryHelper
from db.mongo_wrapper import MongoWrapper


def __analyze_jira():
    prs_cursor = bitbucket_pull_requests_collection.find({"closed": True})

    issue_changelogs = []

    for pr in prs_cursor:
        issue_key = pr["title"].split(':', 1)[0]
        issue_key = issue_key.split(" ", 1)[0]

        matching_issue_changelog = jira_issue_histories_collection.find_one({"key": issue_key})

        if matching_issue_changelog:
            issue_changelogs.append(matching_issue_changelog)

    changelog_counter = 0
    fields = {}

    description_change_counts = {}


    for changelog in issue_changelogs:

        matching_issue = jira_issues_collection.find_one({"key": changelog["key"]})

        description = matching_issue["fields"]["description"]

        if description:

            dict_key = ""

            if "Ziel" in description or "Goal" in description:
                dict_key += "Ziel"
            if "Implementation" in description or "Implementierung" in description or "Umsetzung" in description or  "Konzept" in description or "Concept" in description:
                dict_key += "Implementierung"

        histories = changelog["changelog"]["histories"]

        concept_done_date = datetime.now(timezone.utc)

        description_change_count = 0
        
        for history in histories:
            for item in history["items"]:
                
                history_date = datetime.strptime(history["created"], "%Y-%m-%dT%H:%M:%S.%f%z")

                if item["field"] == "status" and item["toString"] == "In Progress":
                    concept_done_date = history_date

                #DictionaryHelper.add_one_to_dict_counter(fields, item["field"])

                if item["field"] == "description" and concept_done_date < history_date and item["fromString"] and abs(len(item["toString"]) - len(item["fromString"])) >= 5:
                        description_change_count += 1
        
        changelog_counter += 1
        #DictionaryHelper.append_value_to_dict_list(description_change_counts, changelog["project"], description_change_count)
        DictionaryHelper.append_value_to_dict_list(description_change_counts, dict_key, description_change_count)

    print(fields)
    print(changelog_counter)
    print(description_change_counts)

    change_metrics = {}

    for month in description_change_counts:
        change_metrics[month] = list(map(lambda element: {element: description_change_counts[month].count(element)}, set(description_change_counts[month])))

    print(change_metrics)



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

