package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"path"

	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func init() {
	godotenv.Load()
}

func response(c *gin.Context, statusCode int, err error, payload interface{}) {
	var status string
	if statusCode >= 200 && statusCode <= 299 {
		status = "success"
	} else {
		status = "error"
	}
	data := gin.H{
		"code":    statusCode,
		"status":  status,
		"payload": payload,
	}
	if err != nil {
		data["error"] = err.Error()
	}

	c.JSON(statusCode, data)
}

func main() {
	router := gin.Default()

	subject := ""

	router.GET("/fetch", func(c *gin.Context) {
		response(c, http.StatusOK, nil, readFile("files/topics.txt"))
	})

	router.GET("/sub_topic/:name", func(c *gin.Context) {
		name := path.Join("files", c.Param("name"), "sub_topics.txt")
		subject = c.Param("name")
		response(c, http.StatusOK, nil, readFile(name))
	})

	router.GET("/subject/:name", func(c *gin.Context) {
		name := path.Join("files", subject, c.Param("name")+".csv")
		response(c, http.StatusOK, nil, readFile(name))
	})

	router.GET("/refresh", func(c *gin.Context) {
		pull()
		response(c, http.StatusOK, nil, "refreshed")
	})

	router.Use(static.Serve("/", static.LocalFile("ui", true)))
	router.NoRoute(func(c *gin.Context) {
		c.File("./ui/index.html")
	})
	router.Run()

}

func readFile(path string) string {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		fmt.Println("File reading error", err)
		return ""
	}
	return string(data)
}
