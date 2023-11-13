proto-compile:
	protoc --go_out=. --go-grpc_out=require_unimplemented_servers=false:. proto/base_types.proto proto/bot.proto proto/web_api.proto

tests:
	go test ./... -test.v

run:
	go run cmd/main.go --config=config/dev.yml

build:
	go build -o bin/apigateway cmd/main.go
