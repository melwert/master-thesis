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

// GetAllProjects godoc
// @Summary Get all projects
// @Schemes
// @Description placeholder
// @Tags Project
// @Accept json
// @Produce json
// @Success 200 {string} Placeholder
// @Router /projects [get]
func GetAllProjects(ginContext *gin.Context) {

	var projects []models.Project
	projectsCursor, err := mongodb.ProjectsCollection.Find(context.TODO(), bson.M{})
	if err != nil {
		panic(err)
	}

	if err = projectsCursor.All(context.TODO(), &projects); err != nil {
		panic(err)
	}

	projectsCursor.Close(context.TODO())

	ginContext.JSON(http.StatusOK, projects)
}

// GetProjectById godoc
// @Summary Get one project
// @Schemes
// @Description placeholder
// @Tags Project
// @Accept json
// @Produce json
// @Param id   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /projects/:id [get]
func GetProjectById(ginContext *gin.Context) {
	projectId := ginContext.Param("id")

	objectId := utils.GetObjectId(projectId)

	var project models.Project
	err := mongodb.ProjectsCollection.FindOne(context.TODO(), bson.M{"_id": objectId}).Decode(&project)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, project)
}

// GetGeneralStatisticByProjectId godoc
// @Summary Get the general statistics for one project
// @Schemes
// @Description placeholder
// @Tags Project
// @Accept json
// @Produce json
// @Param projectId   path      string  true  "Project Id"
// @Success 200 {string} Placeholder
// @Router /generalStatistics/{projectId} [get]
func GetGeneralStatisticByProjectId(ginContext *gin.Context) {
	projectId := ginContext.Param("projectId")

	objectId := utils.GetObjectId(projectId)

	var generalStatistic models.GeneralStatistic
	err := mongodb.GeneralStatisticsCollection.FindOne(context.TODO(), bson.M{"project_id": objectId}).Decode(&generalStatistic)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, generalStatistic)
}
