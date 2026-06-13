package app

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"relations-service/config"
)

func Run(logger *slog.Logger, cfg *config.Config) {
	container, err := NewContainer(logger, cfg)
	if err != nil {
		logger.Error("failed to initialize application", "error", err)
		os.Exit(1)
	}
	defer func() {
		if container.Rabbit != nil {
			container.Rabbit.Close()
		}
	}()

	ctx, stopConsumer := context.WithCancel(context.Background())
	defer stopConsumer()

	if container.Rabbit != nil {
		go func() {
			if err := container.Rabbit.ConsumeNormalizedDatasets(ctx, container.Service.ProcessNormalizedDataset); err != nil {
				container.Logger.Error("rabbitmq consumer stopped", "error", err)
			}
		}()
	}

	server := &http.Server{
		Addr:    cfg.Server.Port,
		Handler: container.Router(),
	}

	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			container.Logger.Error("server ListenAndServe error", "error", err)
		}
	}()

	container.Logger.Info("server started", "addr", cfg.Server.Port)

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	container.Logger.Info("shutdown signal received")

	shutdownCtx, cancel := context.WithTimeout(context.Background(), cfg.Server.GracefulShutdownTimeout)
	defer cancel()

	if err := server.Shutdown(shutdownCtx); err != nil {
		container.Logger.Warn("server forced to shutdown", "error", err)
	} else {
		container.Logger.Info("server stopped gracefully")
	}
}
