run-flink-job:
	docker exec -d jobmanager flink run -py /flink/jobs/log_job.py

# Stop all containers
stop:
	docker-compose down

# Build and start all containers
start:
	docker-compose up --build -d

# Restart the Flink JobManager
restart-flink:
	docker restart jobmanager taskmanager

restart-postgres:
	docker restart postgres pgadmin