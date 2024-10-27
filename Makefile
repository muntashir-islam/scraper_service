
IMAGE_NAME_SCRAPER = scraper_service
IMAGE_NAME_METRICS = metrics_service
CONTAINER_SCRAPER = scraper_service_container
CONTAINER_METRICS = scraper_service_container
PORT = 8080

# Run the application locally
local-run:
	./scraper/scraper_service.py --listen=0.0.0.0:8080 &


# Stop the locally running scraper_service
local-stop:
	@echo "Stopping local scraper_service.py..."
	@PID=$$(ps aux | grep '[s]craper_service.py' | awk '{print $$2}') && \
	if [ -n "$$PID" ]; then \
		kill $$PID; \
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
	docker run --name $(CONTAINER_SCRAPER) -p $(PORT):8080 $(IMAGE_NAME_SCRAPER)
	docker run --name $(CONTAINER_METRICS) -p $(PORT):9095 $(IMAGE_NAME_METRICS)

# Target to stop the running container
stop:
	docker stop $(CONTAINER_SCRAPER)
	docker stop $(CONTAINER_METRICS)

# Target to remove the stopped container
remove:
	docker rm $(CONTAINER_NAME)

# Target to clean up the Docker image and container
clean: stop remove
	docker rmi $(IMAGE_NAME) || true

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