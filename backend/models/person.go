package models

import (
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Person struct {
	Id          primitive.ObjectID `bson:"_id" json:"id,omitempty"`
	CommitCount int                `bson:"commit_count" json:"commitCount,omitempty"`
	Name        string             `bson:"name" json:"name,omitempty"`
}
