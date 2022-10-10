from db.mongo_wrapper import MongoWrapper


def __analyze_jira():
    prs_cursor = bitbucket_pull_requests_collection.find({"closed": True})

    issue = []

    for pr in prs_cursor:
        issue_key = pr["title"].split(':', 1)[0]
        issue_key = issue_key.split(" ", 1)[0]

        matching_issue_changelog = jira_issues_collection.find_one({"key": issue_key})

        if matching_issue_changelog:
            issue.append(matching_issue_changelog)

    changelog_counter = 0
    fields = {}

    description_change_counts = {}

    containing = 0
    not_containing = 0

    for i in issue:
        description = i["fields"]["description"]

        if description:

            if "Ziel" in description or "Goal" in description or "Goals" in description or "Ziele" in description:
                containing += 1
            else:
                not_containing += 1

    print(containing)
    print(not_containing)



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

