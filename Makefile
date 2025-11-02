include .env
export

.PHONY: up down clean create populate run

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v
	sudo rm -rf ./data

create:
	cat schema_biblioteca.sql | docker exec -i pg_database psql -U $(PG_USER) -d $(PG_DB)

populate:
	cat populate.sql | docker exec -i pg_database psql -U $(PG_USER) -d $(PG_DB)

run:
	python app/main.py