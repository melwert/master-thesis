package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type BoxPlotDataSetSeriesData struct {
	X string    `bson:"x" json:"x"`
	Y []float64 `bson:"y" json:"y"`
}

type BoxPlotDataSetSeries struct {
	Name string                     `bson:"name,omitempty" json:"name,omitempty"`
	Data []BoxPlotDataSetSeriesData `bson:"data" json:"data"`
}

type BoxPlotDataSet struct {
	Id        primitive.ObjectID     `bson:"_id" json:"id,omitempty"`
	Series    []BoxPlotDataSetSeries `bson:"series" json:"series"`
	ProjectId primitive.ObjectID     `bson:"project_id" json:"projectId,omitempty"`
}
