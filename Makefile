format:
	poetry run ruff format .
	poetry run ruff check --fix .

run:
	poetry run uvicorn demo_user_service.api.main:create_app --factory --host 0.0.0.0

run-dev:
	poetry run uvicorn demo_user_service.api.main:create_app --factory --reload

edgedb-instance-link:
	docker compose up db -d
	edgedb instance link demo_user_service_docker --dsn edgedb://edgedb:edgedbPassword@localhost:5656

edgedb-migrate:
	edgedb migration create -I demo_user_service_docker
	edgedb migration apply -I demo_user_service_docker

edgedb-generate:
	poetry run edgedb-py \
		-I demo_user_service_docker \
		--target async \
		--dir ./demo_user_service/service/queries \
		--file ./demo_user_service/service/queries/__init__.py