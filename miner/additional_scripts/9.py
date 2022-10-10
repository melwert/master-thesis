from db.mongo_wrapper import MongoWrapper


def __analyze_jira():
    issue_cursor = jira_issues_collection.find({"project_slug": "ABC"})

    # slugs = []

    # for issue in issue_cursor:
    #     if not issue["project_slug"] in slugs:
    #         slugs.append(issue["project_slug"])

    # print(slugs)

    persons = []

    for issue in issue_cursor:
        if "assignee" in issue["fields"] and issue["fields"]["assignee"] and "displayName" in issue["fields"]["assignee"]:
            assignee = issue["fields"]["assignee"]["displayName"]

            if not assignee in persons:
                persons.append(assignee)

        if "reporter" in issue["fields"] and issue["fields"]["reporter"] and "displayName" in issue["fields"]["reporter"]:
            reporter = issue["fields"]["reporter"]["displayName"]

            if not reporter in persons:
                persons.append(reporter)

        if "creator" in issue["fields"] and issue["fields"]["creator"] and "displayName" in issue["fields"]["creator"]:
            creator = issue["fields"]["creator"]["displayName"]

            if not creator in persons:
                persons.append(creator)
            
    print(persons)


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

