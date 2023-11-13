package main

import (
	"apigateway/cmd/server"
	"apigateway/internal/api"
	"apigateway/internal/config"
	"apigateway/internal/pb"
	"flag"
	"log"
	"os"
)


func main() {
	fs := flag.NewFlagSet("", flag.ExitOnError)
	cfgPath := fs.String("config", "config/example.yml", "grpc address")
	if err := fs.Parse(os.Args[1:]); err != nil {
		log.Fatal(err)
	}
	cfg, err := config.Load(*cfgPath)
	if err != nil {
		log.Fatalf("Error loading config %s: %s", *cfgPath, err.Error())
	}
	if err = cfg.Validate(); err != nil {
		log.Fatalf("Error validate config %s: %s", *cfgPath, err.Error())
	}
	log.Printf("Successfully loaded config %s: %v", *cfgPath, cfg)

	server, err := server.New(cfg)	
	if err != nil {
		log.Fatalf("Error creating grpc server: %s", err.Error())
	}

	{
		stub, err := api.NewDatabaseServiceStub(cfg)
		if err != nil {
			log.Fatalf("Error creating DatabaseServiceStub: %s", err.Error())
		}
		defer stub.Close()
		pb.RegisterDataSenderServer(server.GrpcServer, stub)
	}

	server.Run()
}
