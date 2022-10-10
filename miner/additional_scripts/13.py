from db.mongo_wrapper import MongoWrapper
from git import Repo

from utils.dictionary_helper import DictionaryHelper


def __get_pr_areas(root_path: str):
    slugs = ["ABC-", "DEF-", "GEH-", "IJK-", "LMN-", "OPQ-", "RST-", "UVW-"]

    pr_cursor = bitbucket_pull_requests_collection.find()

    prs_per_project = {}

    for pr in pr_cursor:
        DictionaryHelper.append_value_to_dict_list(prs_per_project, pr["repo_slug"], pr)

    declines_per_area = {}
    declines_per_number_of_changed_areas = {}

    for project in prs_per_project:

        repo = Repo(f"{root_path}/{project}")
        assert not repo.bare

        all_commits = list(repo.iter_commits())


        for pr in prs_per_project[project]:
            pr_slug = pr["title"].split(":", 1)[0]
            
            analyze = False
            for s in slugs:
                if pr_slug.startswith(s):
                    analyze = True

            if analyze:
                matching_commits = list(filter(lambda commit: (commit.message.startswith(pr_slug)), all_commits))

                declined_cursor = bitbucket_pull_request_activities_collection.find({"repo_slug": pr['repo_slug'], "action": "DECLINED", "pr_name": pr['id']})

                declined_count = 0

                changed_areas = []

                for _ in declined_cursor:
                    declined_count += 1

                for commit in matching_commits:
                    files = commit.stats.files.keys()
                    
                    for file in files:

                        if "=>" in file:
                            pass
                        else:
                            if "/" in file:
                                if "Clients" in file:
                                    folder = file.split("/")[2]
                                else:
                                    folder = file.split("/", 1)[0]

                                if not folder in changed_areas:
                                    changed_areas.append(folder)

                DictionaryHelper.append_value_to_dict_list(declines_per_number_of_changed_areas, len(changed_areas), declined_count)
                
                # for area in changed_areas:

                #     DictionaryHelper.append_value_to_dict_list(declines_per_area, area, declined_count)

    # area_metrics = {}

    # for area in declines_per_area:
    #     area_metrics[area] = list(map(lambda element: {element: declines_per_area[area].count(element)}, set(declines_per_area[area])))

    number_of_changed_areas_metrics = {}

    for area in declines_per_number_of_changed_areas:
        number_of_changed_areas_metrics[area] = list(map(lambda element: {element: declines_per_number_of_changed_areas[area].count(element)}, set(declines_per_number_of_changed_areas[area])))

    # print(area_metrics)
    print(number_of_changed_areas_metrics)

    print("Ende")


if __name__ == "__main__":

    mongo_wrapper = MongoWrapper("", "", "mongodb://localhost:27017")
    pi_database = mongo_wrapper.get_database("project_insight")

    bitbucket_pull_requests_collection = pi_database["bitbucket_pull_requests"]
    bitbucket_pull_request_activities_collection = pi_database["bitbucket_pull_request_activities"]

    __get_pr_areas("folder")

