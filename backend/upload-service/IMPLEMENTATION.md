### 1. Start Infrastructure
```bash
cd upload-service
docker-compose up -d
```

### 2. Apply Database Migrations
Use the official Docker migration image so the Postgres driver is available:
```bash
cd upload-service
docker run --rm --network container:upload-service-postgres-1 -v "$(pwd)/migrations:/migrations" migrate/migrate -path=/migrations -database "postgres://postgres:postgres@localhost:5432/upload_db?sslmode=disable" up
```

If you prefer a local CLI, install it first and then run:
```bash
go install github.com/golang-migrate/migrate/v4/cmd/migrate@latest
$GOPATH/bin/migrate -path migrations -database "postgres://postgres:postgres@localhost:5432/upload_db?sslmode=disable" up
```

### 3. Run the Service
```bash
go run cmd/main.go
```

### 4. Test requests
```bash
curl http://localhost:8081/api/datasets/health
# Expected: {"message":"ok"}
```
```bash
# upload csv file
curl -X POST http://localhost:8081/api/datasets/upload -F "file=@test.csv"

# start analysis and send message to rabbit mq
curl -X POST http://localhost:8081/api/analysis/<datasetId>/start

# jon status
curl http://localhost:8081/api/analysis/<jobId>/status
```

### 5. Monitor RabbitMQ
- Visit http://localhost:15672 (guest:guest)
- Go to Exchanges and open `dataset.events`
- Look at the published message count for the `dataset.uploaded` routing key

