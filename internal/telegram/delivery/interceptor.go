package delivery

import (
	"context"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"time"
)

// LoggingInterceptor is a gRPC server interceptor that logs incoming requests using Zap sugared logger.
func LoggingInterceptor(log logrus.FieldLogger) grpc.UnaryServerInterceptor {
	return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler) (interface{}, error) {
		startTime := time.Now()

		log.WithFields(logrus.Fields{
			"method":  info.FullMethod,
			"request": req,
		}).Info("Incoming gRPC request")

		resp, err := handler(ctx, req)
		duration := time.Since(startTime)

		l := log.WithFields(logrus.Fields{
			"method":   info.FullMethod,
			"duration": duration,
		})

		if err != nil {
			l.Errorf("Error while processing gRPC Request: %v", err)
		} else {
			l.Info("Completed gRPC Request")
		}

		// Return the response and error from the handler
		return resp, err
	}
}
