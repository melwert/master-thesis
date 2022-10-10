from typing import List, TypedDict


# according to apexcharts.js


class PiechartDataSet(TypedDict):
    series: List[float]
    labels: List[str]
    project_id: str
