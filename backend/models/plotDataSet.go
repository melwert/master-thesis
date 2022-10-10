package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type PlotDataSetSeriesData struct {
	X string  `bson:"x" json:"x"`
	Y float64 `bson:"y" json:"y"`
}

type PlotDataSetSeries struct {
	Name string                  `bson:"name,omitempty" json:"name,omitempty"`
	Data []PlotDataSetSeriesData `bson:"data" json:"data"`
}

type PlotDataSet struct {
	Id        primitive.ObjectID  `bson:"_id" json:"id,omitempty"`
	Series    []PlotDataSetSeries `bson:"series" json:"series"`
	ProjectId primitive.ObjectID  `bson:"project_id" json:"projectId,omitempty"`
}
