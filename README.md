# scraper_service with Metrics
A flask based web service  to grab the HTTP GET code of  given URLs and expose related Prometheus metrics.
This repository contains a microservice application consisting of a **scraper service** which expose metrics into **metrics service**. The scraper service fetches HTTP GET responses from provided URLs and exposes Prometheus metrics related to these requests through the metrics service.

## Architecture

- **scraper_service**: Listens for POST requests containing URLs, performs HTTP GET requests, and updates Prometheus metrics.
- **metrics_service**: Exposes Prometheus metrics related to the HTTP GET requests made by the scraper service.

## Prerequisites

- Docker
- Docker Compose
- Python 3.11 or higher (for local testing)

## Getting Started

### Build and Run the Services

To build and run all services, run:

```bash
make compose-up
```
This will bring up all the services and start A script to regularly request scraper_service

To check the metrics
```shell
curl localhost:9095/metrics
```

This will show metrics following way
```shell
➜  ~ curl localhost:9095/metrics
# HELP http_get_total Counts HTTP GET requests
# TYPE http_get_total counter
http_get_total{code="200",url="https://phaidra.ai"} 6.0
http_get_total{code="404",url="https://phaidra.ai/trackrecord"} 2.0
http_get_total{code="200",url="https://wikipedia.org"} 1.0
http_get_total{code="200",url="https://github.com"} 2.0
# HELP http_get_created Counts HTTP GET requests
# TYPE http_get_created gauge
http_get_created{code="200",url="https://phaidra.ai"} 1.7299883701981196e+09
http_get_created{code="404",url="https://phaidra.ai/trackrecord"} 1.729988549986851e+09
http_get_created{code="200",url="https://wikipedia.org"} 1.7299885659217694e+09
http_get_created{code="200",url="https://github.com"} 1.7299885711576858e+09
```

You can view this into prometheus server by browsing 
```shell
http://localhost:9090
```
and selecting http_get_total

### Here are some PromQL query to play with this metrics

To find total 404/400 error
```shell
sum(http_get_total{code="404", job="metrics_service"})
```

To find total successful request
```shell
sum(http_get_total{status!~"4.."})
```

Return the 5-minute rate of the http_requests_total metric for the past 30 minutes, with a resolution of 1 minute.
```shell
rate(http_get_total[5m])[30m:1m]
```
Return a whole range of time (in this case 5 minutes up to the query time) for the same vector, making it a range vector
```shell
http_get_created{job="metrics_service"}[5m]
```

To test the unittest cases
```bash
make test
```

### Build and Run the Services without Locally

Ensure that you have python installed with version 3.10 and above
```shell
python --version
```
Set Virtual Environment
```shell
cd scrapper_service
python -m venv venv
source venv/bin/activate

```
Install necessary packages 

```shell
pip install Flask requests prometheus_client
```

To start all services
```shell
make local-start
```
This will start all the services including a script to regularly request scraper_service

To stop services bring another console and run
```shell
make local-stop
```

### Deploy Service into Kubernetes

```shell
kubectl apply -k deployment/kustomize/.
```
As all are clusterIP services, you have to use Port-forward to access these services
```shell
kubectl port-forward svc/scraper-service 9095:9095 #access metrics Service
kubectl port-forward svc/scraper-service 8080:8080 # Access Scraper Services
kubectl port-forward svc/prometheus  9090:9090 #Access Prometheus

```






