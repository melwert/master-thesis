from typing import List, Optional, TypedDict


class Person(TypedDict):
    id: Optional[str]
    commit_count: int
