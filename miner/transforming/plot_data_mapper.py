from numbers import Number
from typing import Dict
from models.piechart_data_set import PiechartDataSet

from models.plot_data_set import PlotDataSet, PlotDataSetSeries, PlotDataSetSeriesData


class PlotDataMapper:

    @staticmethod
    def map_shortlog_result_to_heatmap_dataset(result: Dict) -> Dict:
        heatmap_dataset = PlotDataSet(series=[])
        
        for file in result:

            folder = result[file]["folder"]
            if folder == "":
                folder = "/"

            if not folder in [folder["name"] for folder in heatmap_dataset["series"]]:
                heatmap_dataset["series"].append(PlotDataSetSeries(name=folder, data=[]))

            contributors: Number = result[file]["contributors"]

            matching_series = [series for series in heatmap_dataset["series"] if series["name"] == folder][0]

            for contributor in contributors:
                if not contributor["commiter"] in [data["x"] for data in matching_series["data"]]:
                    data = PlotDataSetSeriesData(
                        x=contributor["commiter"],
                        y=int(contributor["commit_count"])
                    )

                    matching_series["data"].append(data)

                else:
                    matching_data = [data for data in matching_series["data"] if data["x"] == contributor["commiter"]][0]

                    matching_data["y"] += int(contributor["commit_count"])

        return heatmap_dataset

    @staticmethod
    def map_2d_dict_to_heatmap_dataset(twod_dict: Dict) -> Dict:
        plot_dataset = PlotDataSet(series=[])
        
        for row in twod_dict:
            if not row in [series["name"] for series in plot_dataset["series"]]:
                plot_dataset["series"].append(PlotDataSetSeries(name=row, data=[]))

            matching_series = [series for series in plot_dataset["series"] if series["name"] == row][0]

            for column in twod_dict[row]:
                if not column in [data["x"] for data in matching_series["data"]]:
                    data = PlotDataSetSeriesData(
                        x=column,
                        y=twod_dict[row][column]
                    )

                    matching_series["data"].append(data)

                else:
                    matching_data = [data for data in matching_series["data"] if data["x"] == column][0]

                    matching_data["y"] += twod_dict[row][column]

        return plot_dataset

    @staticmethod
    def map_1d_dict_to_heatmap_dataset(oned_dict: Dict) -> Dict:
        series = PlotDataSetSeries(data=[])

        plot_dataset = PlotDataSet(series=[series])
        
        for row in oned_dict:

            matching_datas = [data for data in series["data"] if data["x"] == row]

            if len(matching_datas) == 0:
                data = PlotDataSetSeriesData(
                    x=row,
                    y=oned_dict[row]
                )

                series["data"].append(data)

            else:
                matching_data = matching_datas[0]
                matching_data["y"] += oned_dict[row]

        return plot_dataset

    @staticmethod
    def map_1d_dict_to_piechart_dataset(oned_dict: Dict) -> Dict:
        piechart_dataset = PiechartDataSet(
            series=list(oned_dict.values()),
            labels=list(oned_dict.keys()),
        )

        return piechart_dataset
