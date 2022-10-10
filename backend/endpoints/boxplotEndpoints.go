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

// GetCommitMessageLengthPerAreaByProjectId godoc
// @Summary Get commit message lengths per area statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Boxplots
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /commitMessageLengthAreaBoxplots/{projectId} [get]
func GetCommitMessageLengthPerAreaByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var boxplot models.BoxPlotDataSet
	err := mongodb.CommitMessageLengthAreaBoxplotCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&boxplot)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, boxplot)
}

// GetCommitMessageLengthPerDevByProjectId godoc
// @Summary Get commit message lengths per developer statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Boxplots
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /commitMessageLengthDeveloperBoxplots/{projectId} [get]
func GetCommitMessageLengthPerDevByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var boxplot models.BoxPlotDataSet
	err := mongodb.CommitMessageLengthDeveloperBoxplotCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&boxplot)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, boxplot)
}
