# Variables
JOB_MANAGER_CONTAINER=jobmanager
FLINK_JOB_PATH=/flink/jobs/jobs/log_job.py

# Default command to run the Flink job
run-flink-job:
	docker exec $(JOB_MANAGER_CONTAINER) python $(FLINK_JOB_PATH)

# Helper command to check if JobManager is running
check-jobmanager:
	docker ps --filter "name=$(JOB_MANAGER_CONTAINER)"

# Stop all containers
stop:
	docker-compose down

# Build and start all containers
start:
	docker-compose up --build -d

# Restart the Flink JobManager
restart-jobmanager:
	docker restart $(JOB_MANAGER_CONTAINER)