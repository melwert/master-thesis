from mining.bitbucket_miner import BitbucketMiner
from db.mongo_wrapper import MongoWrapper


def __mine_bitbucket(
    bitbucket_base_url: str,
    bitbucket_project_name: str,
    bitbucket_repo_slug: str,
    bitbucket_username: str,
    bitbucket_password: str,
    start_iteration: int) -> None:

    pr_cursor = bitbucket_pull_requests_collection.find({'repo_slug': bitbucket_repo_slug})

    pull_request_ids = [p['id'] for p in pr_cursor]

    changes = BitbucketMiner.mine_changes(pull_request_ids, bitbucket_base_url, bitbucket_project_name, bitbucket_repo_slug, bitbucket_username, bitbucket_password, sleep_time=5)

    if changes:
        bitbucket_pull_request_changes_collection.insert_many(changes)


if __name__ == "__main__":

    mongo_wrapper = MongoWrapper("", "", "mongodb://localhost:27017")
    pi_database = mongo_wrapper.get_database("project_insight")

    bitbucket_pull_requests_collection = pi_database["bitbucket_pull_requests"]
    bitbucket_pull_request_activities_collection = pi_database["bitbucket_pull_request_activities"]
    bitbucket_pull_request_changes_collection = pi_database["bitbucket_pull_request_changes"]
    jira_issues_collection = pi_database["jira_issues"]
    jira_issue_histories_collection = pi_database["jira_issue_histories"]

    qa_loops_collection = pi_database["bitbucket_qa_loops"]

    pr_count = __mine_bitbucket("", "ABC", "abc", "username", "password", 0)

