package endpoints

import (
	"context"
	"net/http"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"

	"backend/models"
	"backend/mongodb"
	"backend/utils"
)

// GetFileChangesPerAreaByProjectId godoc
// @Summary Get changed files per commit per area statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Barcharts
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /fileChangesAreaBarcharts/{projectId} [get]
func GetFileChangesPerAreaByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var barchart models.PlotDataSet
	err := mongodb.FileChangeHeatmapAreaBarchartCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&barchart)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, barchart)
}

// GetFileChangesPerDevByProjectId godoc
// @Summary Get changed files per commit per developer statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Barcharts
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /fileChangesDeveloperBarcharts/{projectId} [get]
func GetFileChangesPerDevByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var barchart models.PlotDataSet
	err := mongodb.FileChangeHeatmapDeveloperBarchartCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&barchart)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, barchart)
}

// GetCommitHoursByProjectId godoc
// @Summary Get changed files per commit per developer statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Barcharts
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /commitHourBarcharts/{projectId} [get]
func GetCommitHoursByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var barchart models.PlotDataSet
	err := mongodb.CommitHoursBarchartCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&barchart)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, barchart)
}

// GetCommitWeekdaysByProjectId godoc
// @Summary Get changed files per commit per developer statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Barcharts
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /commitWeekdayBarcharts/{projectId} [get]
func GetCommitWeekdaysByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var barchart models.PlotDataSet
	err := mongodb.CommitWeekdaysBarchartCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&barchart)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, barchart)
}
