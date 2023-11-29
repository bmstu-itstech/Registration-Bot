package api

import (
	"apigateway/internal/config"
	"apigateway/internal/pb"
	"context"
	"log"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)


// Stub responsible for database requests
type DatabaseServiceStub struct {
	conn *grpc.ClientConn
}

// Returns new stub
func NewDatabaseServiceStub(cfg *config.Config) (*DatabaseServiceStub, error) {
	conn, err := grpc.Dial(
		cfg.DatabaseService.String(),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return nil, err
	}
	
	return &DatabaseServiceStub{
		conn: conn,
	}, nil
}

// Connection must be closed!
func (stub *DatabaseServiceStub) Close() error {
	return stub.conn.Close()
}

// Relaying a request to a database service
func (stub *DatabaseServiceStub) Create_Bot(ctx context.Context, req *pb.CreateBotRequest) (*pb.CreateBotResponse, error) {
	log.Printf("Got request: %v", req)
	client := pb.NewBotWorkerClient(stub.conn)	
	return client.CreateBot(ctx, req)
}
