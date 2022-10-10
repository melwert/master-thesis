package utils

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

var apiUrl string
var swaggerUrl string

func ConfigureFrontendApiUrl(newApiUrl string, newSwaggerUrl string) {
	apiUrl = newApiUrl
	swaggerUrl = newSwaggerUrl

	err := filepath.Walk("./frontend-dist/_nuxt", setApiUrlInFile)
	if err != nil {
		panic(err)
	}
}

func setApiUrlInFile(path string, fi os.FileInfo, err error) error {
	if err != nil {
		return err
	}

	if fi.IsDir() {
		return nil //
	}

	matched_js, err := filepath.Match("*.js", fi.Name())

	if err != nil {
		panic(err)
	}

	if matched_js {
		read, err := ioutil.ReadFile(path)
		if err != nil {
			panic(err)
		}

		newContents := strings.Replace(string(read), "BASE_URL_STRING_TO_REPLACE", apiUrl, -1)
		newContents = strings.Replace(newContents, "http://localhost:8080/swagger/index.html", swaggerUrl, -1)

		err = ioutil.WriteFile(path, []byte(newContents), 0)
		if err != nil {
			panic(err)
		}

	}

	matched_html, err := filepath.Match("*.html", fi.Name())

	if err != nil {
		panic(err)
	}

	if matched_html {
		read, err := ioutil.ReadFile(path)
		if err != nil {
			panic(err)
		}

		newContents := strings.Replace(string(read), "SWAGGER_URL_STRING_TO_REPLACE", swaggerUrl, -1)

		err = ioutil.WriteFile(path, []byte(newContents), 0)
		if err != nil {
			panic(err)
		}

	}

	return nil
}
