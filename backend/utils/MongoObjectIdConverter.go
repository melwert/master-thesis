package utils

import "go.mongodb.org/mongo-driver/bson/primitive"

func GetObjectId(id string) primitive.ObjectID {
	objectId, err := primitive.ObjectIDFromHex(id)

	if err != nil {
		panic(err)
	}

	return objectId
}
