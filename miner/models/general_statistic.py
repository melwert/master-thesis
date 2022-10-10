from typing import List, TypedDict


class GeneralStatistic(TypedDict):
    commit_count: int
    file_count: int
    developer_count: int
    repository_link: str
    bitbucket_comment_count: int
    bitbucket_pr_count: int
    branch_count: int
    jira_issue_count: int
    fileendings: List[str]
    last_scan_date: str
    project_id: str
