from db.mongo_wrapper import MongoWrapper
from git import Repo

from utils.dictionary_helper import DictionaryHelper


def __analyze_commit_areas(root_path: str):

    # pr_cursor = bitbucket_pull_requests_collection.find()

    # projects = []


    # for pr in pr_cursor:
    #     if not pr["repo_slug"] in projects:
    #         projects.append(pr["repo_slug"])

    projects = ["abc", "def", "geh", "ijk", "lmn", "opq"]

    working_areas_per_dev = {}

    for project in projects:

        repo = Repo(f"{root_path}/{project}")
        assert not repo.bare

        all_commits = list(repo.iter_commits())

        for commit in all_commits:

            files = commit.stats.files.keys()

            for file in files:

                if "=>" in file:
                    pass

                else:
                    if "/" in file:
                        if "/Clients/" in file:
                            folder = file.split("/")[2]
                        else:
                            folder = file.split("/", 1)[0]

                        if "." in folder:
                            folder = folder.split(".", 1)[1]

                if not commit.author.name in working_areas_per_dev:
                    working_areas_per_dev[commit.author.name] = {}

                DictionaryHelper.add_one_to_dict_counter(working_areas_per_dev[commit.author.name], folder)

    for person in working_areas_per_dev:

        print('#####')
        print(person)
        print(working_areas_per_dev[person])


    # for author in working_areas_per_dev:

    #     area_metrics = {}

    #     for area in working_areas_per_dev[author]:
    #         area_metrics[area] = list(map(lambda element: {element: working_areas_per_dev[author][area].count(element)}, set(working_areas_per_dev[author][area])))

    #     print("################")
    #     print(author)
    #     print(area_metrics)

    print("Ende")


if __name__ == "__main__":

    mongo_wrapper = MongoWrapper("", "", "mongodb://localhost:27017")
    pi_database = mongo_wrapper.get_database("project_insight")

    bitbucket_pull_requests_collection = pi_database["bitbucket_pull_requests"]
    bitbucket_pull_request_activities_collection = pi_database["bitbucket_pull_request_activities"]

    __analyze_commit_areas("folder")

