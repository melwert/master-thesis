from datetime import datetime
from typing import Collection, List

from models.project import Project

from models.project_from_file import ProjectFromFile


class ProjectManager():

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_projects_if_nonexistant(projects_collection: Collection, projects: List[ProjectFromFile]) -> None:
        db_projects: List[Project] = projects_collection.find()
        db_project_names = [project["name"] for project in db_projects]


        for project in projects:
            if not project.name in db_project_names:
                new_project = Project(
                    name=project.name,
                    commit_count=0,
                    developer_count=0,
                    file_count=0,
                    last_scan_date=datetime.now(),
                    relevant_file_endings=project.relevant_file_endings,
                    url=project.url,
                    folder_depth=project.folder_depth,
                    issue_count=0,
                    pr_count=0,
                    jira_project_slug=project.jira_project_slug,
                    bitbucket_project_name=project.bitbucket_project_name,
                    bitbucket_repo_slug=project.bitbucket_repo_slug
                )

                projects_collection.insert_one(new_project)
