#####################################################################################################################
# Build and spin up Docker container

docker-build: 
	docker-compose build

sleeper:
	sleep 15

docker-run:
	docker-compose up -d

docker: docker-build sleeper docker-run

shell:
	docker exec -ti etl_pipeline bash

format:
	docker exec etl_pipeline python -m black -S --line-length 79 .

isort:
	docker exec etl_pipeline isort .

pytest:
	docker exec etl_pipeline pytest /code/test

type:
	docker exec etl_pipeline mypy --ignore-missing-imports /code

lint: 
	docker exec etl_pipeline flake8 /code 

ci: isort format type lint pytest

# sudo chmod -R u=rwx,g=rwx,o=rwx scripts test