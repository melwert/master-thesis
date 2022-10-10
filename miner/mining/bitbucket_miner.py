from time import sleep
import time
from typing import Any, List
import requests


class BitbucketMiner:
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def mine_activities(
            pull_request_names: List[str],
            bitbucket_base_url: str,
            bitbucket_project_name: str,
            bitbucket_repo_slug: str,
            bitbucket_username: str,
            bitbucket_password: str,
            sleep_time: int) -> Any:

        iteration = 0

        pull_request_activities = []

        for pull_request_name in pull_request_names:

            if iteration % 100 == 0:
                time.sleep(sleep_time)

            print(f"mining {pull_request_name} ({iteration})")

            end_is_reached = False
            next_page_start = 0

            activities = []

            while not end_is_reached:
                sleep(sleep_time)

                url = f"{bitbucket_base_url}rest/api/1.0/projects/{bitbucket_project_name}/repos/" \
                      f"{bitbucket_repo_slug}/pull-requests/{pull_request_name}/activities?start={next_page_start}"

                response = requests.get(url, auth=(bitbucket_username, bitbucket_password))

                response_json = response.json()

                activities.extend(response_json["values"])

                if response_json["isLastPage"]:
                    end_is_reached = True
                else:
                    if next_page_start != response_json["start"]:
                        print("WARNING: start != current next_page_start")

                    next_page_start = response_json["nextPageStart"]

                    print(f"nextPageStart: {next_page_start}")

            for activity in activities:
                activity['pr_name'] = pull_request_name
                activity['repo_slug'] = bitbucket_repo_slug

            pull_request_activities.extend(activities)

            iteration += 1

        return pull_request_activities

    @staticmethod
    def mine_pull_requests(
            bitbucket_base_url: str,
            bitbucket_project_name: str,
            bitbucket_repo_slug: str,
            bitbucket_username: str,
            bitbucket_password: str,
            page_start_number: int = 0,
            wait_time_in_secs: int = 5) -> Any:

        end_is_reached = False

        next_page_start = page_start_number

        pull_requests = []

        while not end_is_reached:
            sleep(wait_time_in_secs)

            url = f"{bitbucket_base_url}rest/api/1.0/projects/{bitbucket_project_name}/repos/" \
                  f"{bitbucket_repo_slug}/pull-requests?state=ALL&start={next_page_start}"

            response = requests.get(url, auth=(bitbucket_username, bitbucket_password))

            response_json = response.json()

            pull_requests.extend(response_json["values"])

            if response_json["isLastPage"]:
                end_is_reached = True
            else:
                if next_page_start != response_json["start"]:
                    print("WARNING: start != current next_page_start")

                next_page_start = response_json["nextPageStart"]

                print(f"nextPageStart: {next_page_start}")

        for pr in pull_requests:
            pr['repo_slug'] = bitbucket_repo_slug

        return pull_requests
