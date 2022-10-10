package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type PieChartDataSet struct {
	Id        primitive.ObjectID `bson:"_id" json:"id,omitempty"`
	Series    []float64          `bson:"series" json:"series"`
	Labels    []string           `bson:"labels" json:"labels"`
	ProjectId primitive.ObjectID `bson:"project_id" json:"projectId,omitempty"`
}
