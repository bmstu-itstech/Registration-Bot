# Registration Bot: ApiGateway

## Before launching...

1. Create _your_ configuration by copying `config/example.yml`:

```yml
apigateway:
    host: "XXX.XXX.XXX.XXX" # Host that will listen by gateway
    port: 8000              # Port that will listen by gateway
databaseservice:
    host: "XXX.XXX.XXX.XXX" # Host that listens by database service
    port: 8000              # Port that listens by database service
```

2. Check tests:
```bash
make tests
```

## How to start?

Run this command:
```bash
make run
```

Or compile it:
```bash
make build
./bin/apigateway
```
