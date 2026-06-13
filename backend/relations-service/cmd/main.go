package main

import (
	"os"

	"relations-service/config"
	"relations-service/internal/app"
	"relations-service/internal/logger"
)

func main() {
	log := logger.New()

	cfg, err := config.Load()
	if err != nil {
		log.Error("failed to load config", "error", err)
		os.Exit(1)
	}

	app.Run(log, cfg)
}
