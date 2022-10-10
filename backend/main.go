package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/mandrigin/gin-spa/spa"
	"go.mongodb.org/mongo-driver/mongo"

	docs "backend/docs"
	"backend/utils"

	swaggerfiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"

	"backend/endpoints"
	"backend/mongodb"
)

var MongoClient *mongo.Client
var ProjectsCollection *mongo.Collection

func setupRouter(useSwagger bool) *gin.Engine {
	// Disable Console Color
	// gin.DisableConsoleColor()

	// Creates a gin router with default middleware:
	// logger and recovery (crash-free) middleware
	router := gin.Default()

	// default cors = allow all origins, change for production
	router.Use(cors.Default())

	docs.SwaggerInfo.BasePath = "/api"

	// @BasePath /api

	api := router.Group("/api")
	{
		// Ping test
		api.GET("/ping", func(context *gin.Context) {
			context.String(http.StatusOK, "pong")
		})

		api.GET("/projects", endpoints.GetAllProjects)
		api.GET("/projects/:id", endpoints.GetProjectById)
		api.GET("/generalStatistics/:projectId", endpoints.GetGeneralStatisticByProjectId)

		api.GET("/commitHeatmaps/:projectId", endpoints.GetDeveloperHeatmapByProjectId)
		api.GET("/commitMessageLengthHeatmaps/:projectId", endpoints.GetCommitMessageLengthHeatmapByProjectId)

		api.GET("/fileChangesAreaBarcharts/:projectId", endpoints.GetFileChangesPerAreaByProjectId)
		api.GET("/fileChangesDeveloperBarcharts/:projectId", endpoints.GetFileChangesPerDevByProjectId)
		api.GET("/commitHourBarcharts/:projectId", endpoints.GetCommitHoursByProjectId)
		api.GET("/commitWeekdayBarcharts/:projectId", endpoints.GetCommitWeekdaysByProjectId)

		api.GET("/commitMessageLengthAreaBoxplots/:projectId", endpoints.GetCommitMessageLengthPerAreaByProjectId)
		api.GET("/commitMessageLengthDeveloperBoxplots/:projectId", endpoints.GetCommitMessageLengthPerDevByProjectId)

		api.GET("/fileCountAreaPiecharts/:projectId", endpoints.GetFileCountsPerDirectoryByProjectId)

		api.GET("/persons", endpoints.GetAllPersons)
		api.GET("/persons/:id", endpoints.GetPersonById)

		api.GET("/commitHourPersonBarcharts/:personId", endpoints.GetCommitHoursByPersonId)
		api.GET("/commitWeekdayPersonBarcharts/:personId", endpoints.GetCommitWeekdaysByPersonId)
	}

	if useSwagger {
		router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerfiles.Handler))
	}

	// serve frontend directory as spa
	// THIS MUST BE THE LAST MATCHING RULE (it's root ya know)
	router.Use(spa.Middleware("/", "./frontend-dist"))

	return router
}

func main() {
	apiUrl := os.Getenv("API_URL")
	if len(apiUrl) == 0 {
		apiUrl = "http://localhost:8080/api"
	}

	swaggerUrl := os.Getenv("SWAGGER_URL")
	if len(swaggerUrl) == 0 {
		swaggerUrl = "http://localhost:8080/swagger/index.html"
	}

	utils.ConfigureFrontendApiUrl(apiUrl, swaggerUrl)

	connectionString := os.Getenv("CONNECTION_STRING")
	if len(connectionString) == 0 {
		connectionString = "mongodb://192.168.2.2:27017"
	}

	mongodb.InitDbConnection(connectionString)

	useSwaggerParameter := os.Getenv("USE_SWAGGER")
	useSwagger := false
	if len(useSwaggerParameter) == 0 {
		useSwagger = true
	} else {
		useSwagger, _ = strconv.ParseBool(useSwaggerParameter)
	}

	router := setupRouter(useSwagger)

	listenPort := os.Getenv("LISTEN_PORT")
	if len(listenPort) == 0 {
		listenPort = "8080"
	}

	// Listen and Server in 0.0.0.0:<port>
	router.Run(fmt.Sprintf(":%s", listenPort))
}
