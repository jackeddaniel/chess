package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func EchoHandler(c *gin.Context) {
	conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		log.Printf("Failed to set up websocket: %v", err)
		return
	}
	defer conn.Close()

	log.Printf("New client connected from: %s", conn.RemoteAddr())

	for {
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			log.Printf("Read error: %v", err)
			break
		}

		fmt.Printf("Recieved: %s\n", p)

		response := append([]byte("Server echoed (via Gin+Gorilla): "), p...)

		if err := conn.WriteMessage(messageType, response); err != nil {
			log.Printf("Write error: %v", err)
			break
		}
	}
	log.Printf("Client disconnected from: %s", conn.RemoteAddr())

}

func main() {
	router := gin.Default()

	router.Use(cors.New(cors.Config{
		AllowAllOrigins: true,
	}))

	router.GET("/ws", EchoHandler)
	port := ":8080"
	fmt.Printf("Gin server starting on http://localhost%s\n", port)

	if err := router.Run(port); err != nil {
		log.Fatal("Router run error:", err)
	}
}
