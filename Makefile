
IMAGE_NAME_SCRAPER = muntashir/scraper_service
IMAGE_NAME_METRICS = muntashir/metrics_service
CONTAINER_SCRAPER = scraper_service_container
CONTAINER_METRICS = metrics_service_container
PORT1 = 8080
PORT2 = 9095
SCRAPER_TEST_DIR = scraper
METRICS_TEST_DIR = metrics
PYTHON = python3

test: test-scraper test-metrics

test-scraper:
	@echo "Running scraper service tests..."
	$(PYTHON) -m unittest discover -s $(SCRAPER_TEST_DIR) -p "test*"

test-metrics:
	@echo "Running metrics service tests..."
	$(PYTHON) -m unittest discover -s $(METRICS_TEST_DIR) -p "test*"


local-stop: local-stop-scraper local-stop-metrics
# Run the application locally
local-start:
	./scraper/scraper_service.py --listen=0.0.0.0:8080 &
	./metrics/metrics_service.py --listen=0.0.0.0:9095 &


# Stop the locally running scraper_service
local-stop-scraper:
	@echo "Stopping local scraper_service.py..."
	@PID=$$(ps aux | grep '[s]craper_service.py' | awk '{print $$2}') && \
	if [ -n "$$PID" ]; then \
		kill $$PID;  \
		echo "Service stopped." ; \
	else \
		echo "No running service found." ; \
	fi
# Stop the locally running scraper_service
local-stop-metrics:
	@echo "Stopping local metrics_service.py..."
	@PID=$$(ps aux | grep '[m]etrics_service.py' | awk '{print $$2}') && \
	if [ -n "$$PID" ]; then \
		kill $$PID;  \
		echo "Service stopped." ; \
	else \
		echo "No running service found." ; \
	fi

# Target to build the Docker image
build:
	cd scraper && docker build -t $(IMAGE_NAME_SCRAPER) .
	cd metrics && docker build -t $(IMAGE_NAME_METRICS) .

# Target to run the Docker container
run:
	docker run --name $(CONTAINER_SCRAPER) -e METRICS_SERVICE_URL=http://${CONTAINER_METRICS}:9095/increment -p $(PORT1):8080 $(IMAGE_NAME_SCRAPER) & \
	docker run --name $(CONTAINER_METRICS) -p $(PORT2):9095 $(IMAGE_NAME_METRICS)

# Target to stop the running container
stop:
	docker stop $(CONTAINER_SCRAPER)
	docker stop $(CONTAINER_METRICS)

# Target to remove the stopped container
remove:
	docker rm $(CONTAINER_SCRAPER)
	docker rm $(CONTAINER_METRICS)

# Target to clean up the Docker image and container
clean: stop remove
	docker rmi $(IMAGE_NAME_SCRAPER) || true
	docker rmi $(IMAGE_NAME_METRICS) || true

push:
	docker push $(IMAGE_NAME_SCRAPER)
	docker push $(IMAGE_NAME_METRICS)

# Target to build, run, and clean the container
all: clean build run

# Docker Compose targets

# Target to build and run the application using Docker Compose
compose-up:
	docker compose up --build

# Target to stop and remove the containers defined in Docker Compose
compose-down:
	docker compose down

# Target to remove the stopped containers and images from Docker Compose
compose-clean:
	docker compose down --rmi all