from typing import List

class ProjectFromFile():
    def __init__(self, dictionary = None):
        if dictionary is not None:
            for key, value in dictionary.items():
                setattr(self, key, value)

    name: str
    relevant_file_endings: List[str]
    url: str
    private_url: str
    folder_depth: int
    jira_project_slug: str
    bitbucket_project_name: str
    bitbucket_repo_slug: str

