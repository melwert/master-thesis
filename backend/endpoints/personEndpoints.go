package endpoints

import (
	"backend/models"
	"backend/mongodb"
	"backend/utils"
	"context"
	"net/http"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
)

// GetAllPersons godoc
// @Summary Get all persons
// @Schemes
// @Description placeholder
// @Tags Person
// @Accept json
// @Produce json
// @Success 200 {string} Placeholder
// @Router /persons [get]
func GetAllPersons(ginContext *gin.Context) {

	var persons []models.Person
	personsCursor, err := mongodb.PersonsCollection.Find(context.TODO(), bson.M{})
	if err != nil {
		panic(err)
	}

	if err = personsCursor.All(context.TODO(), &persons); err != nil {
		panic(err)
	}

	personsCursor.Close(context.TODO())

	ginContext.JSON(http.StatusOK, persons)
}

// GetPersonById godoc
// @Summary Get one person
// @Schemes
// @Description placeholder
// @Tags Person
// @Accept json
// @Produce json
// @Param id   path      string  true  "Person Id"
// @Success 200 {string} Placeholder
// @Router /persons/:id [get]
func GetPersonById(ginContext *gin.Context) {
	personId := ginContext.Param("id")

	objectId := utils.GetObjectId(personId)

	var person models.Person
	err := mongodb.PersonsCollection.FindOne(context.TODO(), bson.M{"_id": objectId}).Decode(&person)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, person)
}

// GetCommitHoursByPersonId godoc
// @Summary Get changed files per commit per developer statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Barcharts
// @Accept json
// @Produce json
// @Param personId   path      string  true  "Person Id"
// @Success 200 {string} Placeholder
// @Router /commitHourPersonBarcharts/{personId} [get]
func GetCommitHoursByPersonId(ginContext *gin.Context) {
	personId := ginContext.Param("personId")

	objectId := utils.GetObjectId(personId)

	var barchart models.PlotDataSet
	err := mongodb.CommitHoursPersonBarchartCollection.FindOne(context.TODO(), bson.M{"person_id": objectId}).Decode(&barchart)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, barchart)
}

// GetCommitWeekdaysByPersonId godoc
// @Summary Get changed files per commit per developer statistics in boxplot format
// @Schemes
// @Description placeholder
// @Tags Barcharts
// @Accept json
// @Produce json
// @Param personId   path      string  true  "Person Id"
// @Success 200 {string} Placeholder
// @Router /commitWeekdayPersonBarcharts/{personId} [get]
func GetCommitWeekdaysByPersonId(ginContext *gin.Context) {
	personId := ginContext.Param("personId")

	objectId := utils.GetObjectId(personId)

	var barchart models.PlotDataSet
	err := mongodb.CommitWeekdaysPersonBarchartCollection.FindOne(context.TODO(), bson.M{"person_id": objectId}).Decode(&barchart)

	if err != nil {
		panic(err)
	}

	ginContext.JSON(http.StatusOK, barchart)
}
