from mining.jira_miner import JiraMiner
from db.mongo_wrapper import MongoWrapper


def __mine_jira(
    jira_base_url: str,
    jira_project_slug: str,
    jira_username: str,
    jira_password: str,):        

    # issues = JiraMiner.get_all_issues(jira_base_url, jira_project_slug, jira_username, jira_password, 0)

    # if issues:
    #     jira_issues_collection.insert_many(issues)

    issues = jira_issues_collection.find({"project_slug": "ABC"})

    issue_ids = [i['id'] for i in issues]

    changelog = JiraMiner.mine_issue_changelogs(issue_ids, jira_base_url, jira_username, jira_password, jira_project_slug, jira_issue_changelogs_collection)

    if changelog:
        jira_issue_changelogs_collection.insert_many(changelog)


if __name__ == "__main__":

    mongo_wrapper = MongoWrapper("", "", "mongodb://localhost:27017")
    pi_database = mongo_wrapper.get_database("project_insight")

    jira_issues_collection = pi_database["jira_issues"]
    jira_issue_changelogs_collection = pi_database["jira_issue_histories"]

    pr_count = __mine_jira("https://jira.example.com/", "ABC", "username", "password")

