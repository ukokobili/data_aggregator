#####################################################################################################################
# Build and spin up Docker container

docker-build: 
	docker-compose --env-file env up --build -d

sleeper:
	sleep 15

docker: docker-build sleeper 

shell:
	docker exec -ti etl_pipeline sh

down:
	docker compose --env-file env down

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