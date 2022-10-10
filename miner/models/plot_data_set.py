from typing import List, TypedDict


# according to apexcharts.js

class PlotDataSetSeriesData(TypedDict):
    x: str
    y: int


class PlotDataSetSeries(TypedDict):
    name: str
    data: List[PlotDataSetSeriesData]


class PlotDataSet(TypedDict):
    series: List[PlotDataSetSeries]
    project_id: str
