#####################################################################################################################
# Build and spin up docker contain

docker-build:
	docker-compose build

sleeper:
	sleep 15

docker-run:
	docker-compose run --rm etl_pipeline

docker:	docker-build sleeper docker-run