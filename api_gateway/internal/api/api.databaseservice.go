package api

import (
	"apigateway/internal/config"
	"apigateway/internal/pb"
	"context"
	"log"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)


type DatabaseServiceStub struct {
	conn *grpc.ClientConn
}


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


func (stub *DatabaseServiceStub) Close() error {
	return stub.conn.Close()
}


func (stub *DatabaseServiceStub) Create_Bot(ctx context.Context, req *pb.CreateBotRequest) (*pb.CreateBotResponse, error) {
	log.Printf("Got request: %v", req)
	client := pb.NewBotWorkerClient(stub.conn)	
	return client.CreateBot(ctx, req)
}
