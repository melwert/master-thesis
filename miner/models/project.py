from datetime import datetime
from typing import List, Optional, TypedDict


class Project(TypedDict):
    id: Optional[str]
    name: str
    commit_count: int
    developer_count: int
    file_count: int
    relevant_file_endings: List[str]
    last_scan_date: datetime
    url: str
    folder_depth: int
    issue_count: int
    pr_count: int
    jira_project_slug: str
    bitbucket_project_name: str
    bitbucket_repo_slug: str
