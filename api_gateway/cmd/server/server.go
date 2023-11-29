package server

import (
	"apigateway/internal/config"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"

	"github.com/oklog/oklog/pkg/group"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

type ApiGatewayServer struct {
	address     config.Address
	GrpcServer *grpc.Server
}


// Returns conifgured server structure
func New(cfg *config.Config) (*ApiGatewayServer, error) {

	grpcServer := grpc.NewServer()
	reflection.Register(grpcServer)
	
	return &ApiGatewayServer{
		address:    cfg.ApiGateway,
		GrpcServer: grpcServer,
	}, nil
}

// Run gRPC server to accept requests from the frontend
func (server *ApiGatewayServer) Run() {
	var g group.Group
	{
		listener, err := net.Listen("tcp", server.address.String())
		if err != nil {
			log.Fatalf("Error listening %s: %s", server.address.String(), err.Error())
			return
		}
		log.Printf("Serving address %s", server.address.String())

		g.Add(func() error {
			return server.GrpcServer.Serve(listener)
		}, func(error) {
			listener.Close()
		})
	}
	{
		cancelInterrupt := make(chan struct{})
		g.Add(func() error {
			c := make(chan os.Signal, 1)
			signal.Notify(c, syscall.SIGINT, syscall.SIGTERM)
			select {
			case sig := <-c:
				return fmt.Errorf("received signal %s", sig)
			case <-cancelInterrupt:
				return nil
			}
		}, func(error) {
			close(cancelInterrupt)
		})
	}

	if err := g.Run(); err != nil {
		log.Fatalf("RuntimeError: %s", err.Error())
		return
	}
}
