package mongodb

import (
	"context"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

var MongoClient *mongo.Client
var ProjectsCollection *mongo.Collection
var GeneralStatisticsCollection *mongo.Collection

var CommitHeatmapCollection *mongo.Collection
var FileChangeHeatmapCollection *mongo.Collection
var CommitMessageLengthHeatmapCollection *mongo.Collection

var FileChangeHeatmapAreaBarchartCollection *mongo.Collection
var FileChangeHeatmapDeveloperBarchartCollection *mongo.Collection
var CommitHoursBarchartCollection *mongo.Collection
var CommitWeekdaysBarchartCollection *mongo.Collection

var CommitMessageLengthAreaBoxplotCollection *mongo.Collection
var CommitMessageLengthDeveloperBoxplotCollection *mongo.Collection

var FileCountPerAreaPiechartCollection *mongo.Collection

var PersonsCollection *mongo.Collection

var CommitHoursPersonBarchartCollection *mongo.Collection
var CommitWeekdaysPersonBarchartCollection *mongo.Collection

func InitDbConnection(connectionString string) {

	// Create a new client and connect to the server
	client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(connectionString))

	if err != nil {
		panic(err)
	}

	// Ping the primary
	if err := client.Ping(context.TODO(), readpref.Primary()); err != nil {
		panic(err)
	}

	MongoClient = client
	ProjectsCollection = MongoClient.Database("project_insight").Collection("projects")
	GeneralStatisticsCollection = MongoClient.Database("project_insight").Collection("general_statistics")

	CommitHeatmapCollection = MongoClient.Database("project_insight").Collection("commit_heatmaps")
	FileChangeHeatmapCollection = MongoClient.Database("project_insight").Collection("file_change_heatmaps")
	CommitMessageLengthHeatmapCollection = MongoClient.Database("project_insight").Collection("commit_message_length_heatmaps")

	FileChangeHeatmapAreaBarchartCollection = MongoClient.Database("project_insight").Collection("file_changes_per_area_barchart")
	FileChangeHeatmapDeveloperBarchartCollection = MongoClient.Database("project_insight").Collection("file_changes_per_dev_barchart")
	CommitHoursBarchartCollection = MongoClient.Database("project_insight").Collection("commit_hours_barchart")
	CommitWeekdaysBarchartCollection = MongoClient.Database("project_insight").Collection("commit_weekdays_barchart")

	CommitMessageLengthAreaBoxplotCollection = MongoClient.Database("project_insight").Collection("commit_message_lengths_per_area_boxplot")
	CommitMessageLengthDeveloperBoxplotCollection = MongoClient.Database("project_insight").Collection("commit_message_lengths_per_dev_boxplot")

	FileCountPerAreaPiechartCollection = MongoClient.Database("project_insight").Collection("file_count_per_directory_piechart")

	PersonsCollection = MongoClient.Database("project_insight").Collection("persons")

	CommitHoursPersonBarchartCollection = MongoClient.Database("project_insight").Collection("persons_commit_hours")
	CommitWeekdaysPersonBarchartCollection = MongoClient.Database("project_insight").Collection("persons_commit_weekdays")
}

func DisconnectDbConnection() {
	defer func() {
		if err := MongoClient.Disconnect(context.TODO()); err != nil {
			panic(err)
		}
	}()
}
