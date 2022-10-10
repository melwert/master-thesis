from datetime import datetime
import os
from typing import List
from mining.bitbucket_miner import BitbucketMiner
from mining.jira_miner import JiraMiner
from mining.repo_miner import RepoMiner
from models.appsettings import Appsettings
from models.general_statistic import GeneralStatistic
from models.person import Person
from models.project import Project
from models.project_from_file import ProjectFromFile
from project_manager import ProjectManager
from transforming.plot_data_mapper import PlotDataMapper
from utils.dictionary_helper import DictionaryHelper
from utils.file_loader import FileLoader
from db.mongo_wrapper import MongoWrapper


def __mine_git(project: Project, private_url: str, issue_count: int, pr_count: int) -> None:
    repo_name = repo_miner.checkout_repository(private_url)

    file_count, file_count_per_directory = repo_miner.get_file_infos(repo_name, db_project["folder_depth"])
    
    file_changes_per_area, \
        file_changes_per_dev, \
        file_changes_per_area_and_dev, \
        commit_message_lengths_per_area, \
        commit_message_lengths_per_dev, \
        commit_message_lengths_per_area_and_dev, \
        commit_hours, \
        commit_weekdays, \
        commit_hours_per_author, \
        commit_weekdays_per_author, \
        persons, \
        commit_count = repo_miner.get_changes(repo_name, "master", db_project["folder_depth"])

    update_dict = {
        "commit_count": commit_count,
        "file_count": file_count,
        "developer_count": len(persons.keys()),
        "last_scan_date": datetime.utcnow().isoformat("T") + "Z",
        "issue_count": issue_count,
        "pr_count": pr_count
    }

    general_statistic = GeneralStatistic(
        commit_count = commit_count,
        file_count = file_count,
        developer_count = len(persons.keys()),
        repository_link = db_project["url"],
        bitbucket_comment_count = 0,
        bitbucket_pr_count = 0,
        branch_count = 0,
        jira_issue_count = 0,
        fileendings = [],
        last_scan_date = datetime.utcnow().isoformat("T") + "Z",
        project_id = db_project["_id"]
    )

    projects_collection.update_one({"_id": db_project["_id"]}, {"$set": update_dict})
    general_statistics_collection.update_one({"project_id": db_project["_id"]}, {"$set": general_statistic}, upsert=True)

    commit_changes_heatmap_dataset = PlotDataMapper.map_2d_dict_to_heatmap_dataset(file_changes_per_area_and_dev)
    commit_changes_heatmap_dataset["project_id"] = db_project["_id"]
    commit_heatmap_collection.update_one({"project_id": db_project["_id"]}, {"$set": commit_changes_heatmap_dataset}, upsert=True)

    commit_message_lengths_heatmap_data = PlotDataMapper.map_2d_dict_to_heatmap_dataset(commit_message_lengths_per_area_and_dev)
    commit_message_length_heatmaps_collection.update_one({"project_id": db_project["_id"]}, {"$set": commit_message_lengths_heatmap_data}, upsert=True)

    file_changes_per_area_plot = PlotDataMapper.map_1d_dict_to_heatmap_dataset(file_changes_per_area)
    file_changes_per_dev_plot = PlotDataMapper.map_1d_dict_to_heatmap_dataset(file_changes_per_dev)
    commit_message_lengths_per_area_plot = PlotDataMapper.map_1d_dict_to_heatmap_dataset(commit_message_lengths_per_area)
    commit_message_lengths_per_dev_plot = PlotDataMapper.map_1d_dict_to_heatmap_dataset(commit_message_lengths_per_dev)

    file_changes_per_area_barchart_collection.update_one({"project_id": db_project["_id"]}, {"$set": file_changes_per_area_plot}, upsert=True)
    file_changes_per_dev_barchart_collection .update_one({"project_id": db_project["_id"]}, {"$set": file_changes_per_dev_plot}, upsert=True)
    commit_message_lengths_per_area_boxplot_collection.update_one({"project_id": db_project["_id"]}, {"$set": commit_message_lengths_per_area_plot}, upsert=True)
    commit_message_lengths_per_dev_boxplot_collection.update_one({"project_id": db_project["_id"]}, {"$set": commit_message_lengths_per_dev_plot}, upsert=True)

    commit_hours_plot = PlotDataMapper.map_1d_dict_to_heatmap_dataset(commit_hours)
    commit_weekdays_plot = PlotDataMapper.map_1d_dict_to_heatmap_dataset(commit_weekdays)

    commit_hours_barchart_collection.update_one({"project_id": db_project["_id"]}, {"$set": commit_hours_plot}, upsert=True)
    commit_weekdays_barchart_collection.update_one({"project_id": db_project["_id"]}, {"$set": commit_weekdays_plot}, upsert=True)

    file_count_per_directory_plot = PlotDataMapper.map_1d_dict_to_piechart_dataset(file_count_per_directory)
    file_count_per_directory_piechart_collection.update_one({"project_id": db_project["_id"]}, {"$set": file_count_per_directory_plot}, upsert=True)

    #repo_miner.remove_repository(repo_name)

    return commit_hours_per_author, commit_weekdays_per_author, persons

def __mine_jira(jira_base_url: str, jira_project_slug: str, jira_username: str, jira_password: str, start_iteration: int) -> None:

    issues, issue_count = JiraMiner.get_all_issues(jira_base_url, jira_project_slug, jira_username, jira_password, start_iteration)

    if issues:
        jira_issues_collection.insert_many(issues)

    issue_keys = [i['key'] for i in issues]

    issue_histories = JiraMiner.mine_issue_changelogs(issue_keys, jira_base_url, jira_username, jira_password, jira_project_slug)

    if issue_histories:
        jira_issue_histories_collection.insert_many(issue_histories)

    return issue_count

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
        bitbucket_pull_request_activity_collection.insert_many(activities)

    return len(pull_requests)

def __get_env_vars() -> Appsettings:
    appsettings = Appsettings()

    if "CONNECTION_STRING" in os.environ:
        appsettings.connection_string = os.environ['CONNECTION_STRING']
    else:
        appsettings.connection_string = "mongodb://mongodb:27017"

    if "WORKING_DIR" in os.environ:
        if os.environ['WORKING_DIR'] == "home":
            appsettings.working_dir = os.environ['HOME']
        else:
            appsettings.working_dir = os.environ['WORKING_DIR']
    else:
        appsettings.working_dir = f"{os.environ['HOME']}/git/pi-works"

    if "MINE_JIRA" in os.environ:
        appsettings.mine_jira = os.environ['MINE_JIRA']
    else:
        appsettings.mine_jira = ""

    return appsettings


if __name__ == "__main__":
    appsettings = __get_env_vars()

    projects: List = FileLoader.load_json_list_as_class_instance_list("projects.json", ProjectFromFile)
    repo_miner = RepoMiner(appsettings.working_dir)

    mongo_wrapper = MongoWrapper("", "", appsettings.connection_string)
    pi_database = mongo_wrapper.get_database("project_insight")

    projects_collection = pi_database["projects"]
    commits_by_developer_collection = pi_database["commits_by_developer"]
    general_statistics_collection = pi_database["general_statistics"]

    commit_heatmap_collection = pi_database["commit_heatmaps"]
    commit_message_length_heatmaps_collection = pi_database["commit_message_length_heatmaps"]

    file_changes_per_area_barchart_collection = pi_database["file_changes_per_area_barchart"]
    file_changes_per_dev_barchart_collection = pi_database["file_changes_per_dev_barchart"]
    commit_hours_barchart_collection = pi_database["commit_hours_barchart"]
    commit_weekdays_barchart_collection = pi_database["commit_weekdays_barchart"]

    commit_message_lengths_per_area_boxplot_collection = pi_database["commit_message_lengths_per_area_boxplot"]
    commit_message_lengths_per_dev_boxplot_collection = pi_database["commit_message_lengths_per_dev_boxplot"]

    file_count_per_directory_piechart_collection = pi_database["file_count_per_directory_piechart"]

    bitbucket_pull_requests_collection = pi_database["bitbucket_pull_requests"]
    bitbucket_pull_request_activity_collection = pi_database["bitbucket_pull_request_activities"]
    jira_issues_collection = pi_database["bitbucket_pull_requests"]
    jira_issue_histories_collection = pi_database["jira_issue_histories"]

    persons_collection = pi_database["persons"]
    persons_commit_hours_collection = pi_database["persons_commit_hours"]
    persons_commit_weekdays_collection = pi_database["persons_commit_weekdays"]

    ProjectManager.create_projects_if_nonexistant(projects_collection, projects)

    db_projects: List[Project] = projects_collection.find()

    all_commit_hours = {}
    all_commit_weekdays = {}
    all_persons = {}

    for db_project in db_projects:

        private_url = [p.private_url for p in projects if p.url == db_project["url"]][0]

        # if True:
        #     issue_count = __mine_jira(appsettings.jira_base_url, db_project['jira_project_slug'], appsettings.jira_username, appsettings.jira_password, db_project['issue_count'])

        # if True:
        #     pr_count = __mine_bitbucket(appsettings.bitbucket_base_url, db_project['bitbucket_project_name'], db_project['bitbucket_repo_slug'], appsettings.bitbucket_username, appsettings.bitbucket_password, db_project['pr_count'])

        #__mine_git(db_project, private_url, issue_count, pr_count)
        commit_hours_per_author, commit_weekdays_per_author, persons = __mine_git(db_project, private_url, 0, 0)

        if len(all_commit_hours.keys()) == 0:
            all_commit_hours = commit_hours_per_author
        else:
            for key in commit_hours_per_author:
                if not key in all_commit_hours:
                    all_commit_hours[key] = commit_hours_per_author[key]
                else:
                    DictionaryHelper.join_matching_number_dicts(all_commit_hours[key], commit_hours_per_author[key])

        if len(all_commit_weekdays.keys()) == 0:
            all_commit_weekdays = commit_weekdays_per_author
        else:
            for key in commit_weekdays_per_author:
                if not key in all_commit_weekdays:
                    all_commit_weekdays[key] = commit_weekdays_per_author[key]
                else:
                    DictionaryHelper.join_matching_number_dicts(all_commit_weekdays[key], commit_weekdays_per_author[key])
        
        if len(all_persons.keys()) == 0:
            all_persons = persons
        else:
            for key in persons:
                if not key in all_persons:
                    all_persons[key] = {}
                    all_persons[key]["commit_count"] = persons[key]["commit_count"]
                else:
                    all_persons[key]["commit_count"] += persons[key]["commit_count"]

    db_persons: List[Person] = persons_collection.find()
    db_project_names = [person["name"] for person in db_persons]

    for p in all_persons:
        matching_persons: List[Person] = list(filter(lambda db_person: db_person["name"] == p["name"], db_persons))
        assert(len(matching_persons) <= 1)

        if len(matching_persons) == 0:
            new_person = Person(
                name=p,
                commit_count=all_persons[p]["commit_count"]
            )

            persons_collection.insert_one(new_person)
        
        if len(matching_persons) == 1:
            existing_person = matching_persons[0]
            existing_person["commit_count"] += all_persons[p]["commit_count"]

            persons_collection.update_one({}, {"$set": existing_person}, upsert=True)

    db_persons = persons_collection.find()

    for p in db_persons:
        commit_hour_plot = PlotDataMapper.map_1d_dict_to_heatmap_dataset(all_commit_hours[p["name"]])
        commit_weekday_plot = PlotDataMapper.map_1d_dict_to_heatmap_dataset(all_commit_weekdays[p["name"]])

        persons_commit_hours_collection.update_one({"person_id": p["_id"]}, {"$set": commit_hour_plot}, upsert=True)
        persons_commit_weekdays_collection.update_one({"person_id": p["_id"]}, {"$set": commit_weekday_plot}, upsert=True)
