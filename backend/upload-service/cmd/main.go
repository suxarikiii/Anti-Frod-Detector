package main

import (
	"os"

	"upload-service/config"
	"upload-service/internal/app"
	"upload-service/internal/logger"
)

func main() {
	logger := logger.New()

	cfg, err := config.Load()
	if err != nil {
		logger.Error("failed to load config", "error", err)
		os.Exit(1)
	}

	app.Run(logger, cfg)
}
