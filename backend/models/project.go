package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Project struct {
	Id             primitive.ObjectID `bson:"_id" json:"id,omitempty"`
	CommitCount    int                `bson:"commit_count" json:"commitCount,omitempty"`
	DeveloperCount int                `bson:"developer_count" json:"developerCount,omitempty"`
	FileCount      int                `bson:"file_count" json:"fileCount,omitempty"`
	LastScanDate   time.Time          `bson:"last_scan_date" json:"lastScanDate,omitempty"`
	Name           string             `bson:"name" json:"name,omitempty"`
	Url            string             `bson:"url" json:"url,omitempty"`
}
