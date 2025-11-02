include .env
export

.PHONY: up down clean

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v
	sudo rm -rf $(PG_DIR)
