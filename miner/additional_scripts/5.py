from mining.bitbucket_miner import BitbucketMiner
from utils.dictionary_helper import DictionaryHelper
from db.mongo_wrapper import MongoWrapper


def __mine_bitbucket(
    bitbucket_base_url: str,
    bitbucket_project_name: str,
    bitbucket_repo_slug: str,
    bitbucket_username: str,
    bitbucket_password: str,
    start_iteration: int) -> None:

    pull_requests = BitbucketMiner.mine_pull_requests(bitbucket_base_url, bitbucket_project_name, bitbucket_repo_slug, bitbucket_username, bitbucket_password, page_start_number=start_iteration)

    if pull_requests:
        bitbucket_pull_requests_collection.insert_many(pull_requests)

    pull_request_ids = [p['id'] for p in pull_requests]

    activities = BitbucketMiner.mine_activities(pull_request_ids, bitbucket_base_url, bitbucket_project_name, bitbucket_repo_slug, bitbucket_username, bitbucket_password, sleep_time=5)

    if activities:
        bitbucket_pull_request_activities_collection.insert_many(activities)

    return len(pull_requests)

def __analyze_bitbucket():

    declined_comments = 0
    non_declined_comments = 0

    declined_tasks = 0
    non_declined_tasks = 0

    pr_cursor = bitbucket_pull_requests_collection.find({"closed": True})

    prs_projects = {}
    prop_per_proj = {}

    declined_count = 0
    non_declined_count = 0

    for pr in pr_cursor:
        declined_cursor = bitbucket_pull_request_activities_collection.find({"repo_slug": pr['repo_slug'], "action": "DECLINED", "pr_name": pr['id']})

        declined = False

        for decline in declined_cursor:
            declined = True

        if declined:
            declined_comments += pr["properties"]["commentCount"]
            declined_tasks += pr["properties"]["resolvedTaskCount"]
            declined_tasks += pr["properties"]["openTaskCount"]
            declined_count += 1
        else:
            non_declined_comments += pr["properties"]["commentCount"]
            non_declined_tasks += pr["properties"]["resolvedTaskCount"]
            non_declined_tasks += pr["properties"]["openTaskCount"]
            non_declined_count += 1

        DictionaryHelper.append_value_to_dict_list(prs_projects, pr['repo_slug'], pr)

    print(declined_comments)
    print(declined_tasks)
    print(non_declined_comments)
    print(non_declined_tasks)

    print("###")
    print(declined_count)
    print(non_declined_count)
    print("###")

    for project in prs_projects:

        for pr in prs_projects[project]:
                
            #declined_cursor = bitbucket_pull_request_activities_collection.find({"repo_slug": project, "action": "DECLINED", "pr_name": pr['id']})

            #for _ in declined_cursor:
            #    declined_count += 1

            v = pr["properties"]["resolvedTaskCount"]
            v += pr["properties"]["openTaskCount"]

            DictionaryHelper.append_value_to_dict_list(prop_per_proj, project, v)

    month_metrics = {}

    for month in prop_per_proj:
        month_metrics[month] = list(map(lambda element: {element: prop_per_proj[month].count(element)}, set(prop_per_proj[month])))

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

