
IMAGE_NAME = scraper_service
CONTAINER_NAME = scraper_service_container
PORT = 8080

# Run the application locally
local-run:
	./scraper_service.py --listen=0.0.0.0:8080 &

# Stop the locally running scraper_service
local-remove:
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
	docker build -t $(IMAGE_NAME) .

# Target to run the Docker container
run:
	docker run --name $(CONTAINER_NAME) -p $(PORT):8080 $(IMAGE_NAME)

# Target to stop the running container
stop:
	docker stop $(CONTAINER_NAME)

# Target to remove the stopped container
remove:
	docker rm $(CONTAINER_NAME)

# Target to clean up the Docker image and container
clean: stop remove
	docker rmi $(IMAGE_NAME) || true

# Target to build, run, and clean the container
all: clean build run