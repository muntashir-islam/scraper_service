FROM python:3.9-slim AS build
LABEL authors="muntashir"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Final Stage
FROM python:3.9-slim
WORKDIR /app
# Copy the installed packages from the build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin/* /usr/local/bin/

# Create a non-root user
RUN useradd -m appuser

# Change ownership of the working directory
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Copy the application code into the container
COPY scraper_service.py .

# Expose the port the service will run on
EXPOSE 8080

# Command to run the application
CMD ["python", "scraper_service.py", "--listen=0.0.0.0:8080"]