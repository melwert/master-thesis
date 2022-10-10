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

// GetDeveloperHeatmapByProjectId godoc
// @Summary Get number of commits per area and developer in plot format
// @Schemes
// @Description placeholder
// @Tags Heatmaps
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /commitHeatmaps/{projectId} [get]
func GetDeveloperHeatmapByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var commitHeatmap models.PlotDataSet
	err := mongodb.CommitHeatmapCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&commitHeatmap)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, commitHeatmap)
}

// GetCommitMessageLengthHeatmapByProjectId godoc
// @Summary Get commit message lengths  per area and developer in plot format
// @Schemes
// @Description placeholder
// @Tags Heatmaps
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /commitMessageLengthHeatmaps/{projectId} [get]
func GetCommitMessageLengthHeatmapByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var commitHeatmap models.PlotDataSet
	err := mongodb.CommitMessageLengthHeatmapCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&commitHeatmap)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, commitHeatmap)
}
