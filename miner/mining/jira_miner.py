import re
from time import sleep
from typing import Any, List
import requests


class JiraMiner:
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def mine_issue_changelogs(jira_issue_names: List[str], jira_base_url: str, username: str, password: str, jira_project_name: str) -> Any:

        issue_changelogs = [JiraMiner.mine_changelog(
            issue_name, jira_base_url, username, password, jira_project_name) for issue_name in jira_issue_names]

        return issue_changelogs

    @staticmethod
    def mine_changelog(issue_name: str, jira_base_url: str, username: str, password: str, jira_project_name: str) -> Any:  

        print(f"mining {issue_name}")

        url = f"{jira_base_url}rest/api/2/issue/{issue_name}?expand=changelog"

        response = requests.get(url, auth=(username, password))

        request_json = response.json()

        request_json["project"] = jira_project_name

        sleep(5)

        return request_json

    @staticmethod
    def mine_issues() -> None:

        issue_count = JiraMiner.get_issue_count()

        JiraMiner.get_all_issues(issue_count)

    @staticmethod
    def get_issue_count(jira_base_url: str, jira_project_slug: str, username: str, password: str) -> Any:

        url = f"{jira_base_url}rest/api/2/search?jql=project={jira_project_slug}&maxResults=0"

        response = requests.get(url, auth=(username, password))

        request_json = response.json()

        return request_json["total"]

    @staticmethod
    def get_all_issues(jira_base_url: str, jira_project_slug: str, username: str, password: str, start_iteration: int, wait_time_in_secs: int = 5) -> Any:

        issue_count = 0

        end_is_reached = False

        iteration = start_iteration

        issues = []

        # for iteration in range(start_index, number_of_iterations):
        while not end_is_reached:
            # print(x)

            url = f"{jira_base_url}rest/api/2/search?jql=project=" \
                  f"{jira_project_slug}&maxResults={50}&startAt={iteration}"

            response = requests.get(url, auth=(username, password))

            response_json = response.json()

            if issue_count == 0:
                issue_count = response_json["total"]

            issues.extend(response_json["issues"])

            print(f"iteration {iteration}")

            sleep(wait_time_in_secs)

            iteration += 50

            if iteration > issue_count:
                end_is_reached = True

        for issue in issues:
            issue["project_slug"] = jira_project_slug

        return issues, issue_count
