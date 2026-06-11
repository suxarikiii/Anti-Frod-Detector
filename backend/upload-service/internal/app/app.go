package app

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"upload-service/config"
)

func Run(logger *slog.Logger, cfg *config.Config) {
	container, err := NewContainer(logger, cfg)
	if err != nil {
		logger.Error("failed to initialize application", "error", err)
		os.Exit(1)
	}
	defer func() {
		_ = container.DB.Close()
		container.RabbitPublisher.Close()
	}()

	router := container.Router()
	server := &http.Server{
		Addr:    cfg.Server.Port,
		Handler: router,
	}

	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			container.Logger.Error("Server ListenAndServe error", "error", err)
		}
	}()

	container.Logger.Info("Server started", "addr", cfg.Server.Port)

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	container.Logger.Info("Shutdown signal received")

	ctx, cancel := context.WithTimeout(context.Background(), cfg.Server.GracefulShutdownTimeout)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		container.Logger.Warn("Server forced to shutdown", "error", err)
	} else {
		container.Logger.Info("Server stopped gracefully")
	}
}
