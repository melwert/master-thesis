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

// GetFileCountsPerDirectoryByProjectId godoc
// @Summary Get changed files per commit per area statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Piecharts
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /fileCountAreaPiecharts/{projectId} [get]
func GetFileCountsPerDirectoryByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var barchart models.PieChartDataSet
	err := mongodb.FileCountPerAreaPiechartCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&barchart)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, barchart)
}
