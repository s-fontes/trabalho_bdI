include .env
export

.PHONY: up down clean fix-perms create-dirs rebuild shell

up: create-dirs fix-perms
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v
	sudo rm -rf $(PG_DIR) $(PG_DIR)

rebuild:
	docker compose build --no-cache app

create-dirs:
	mkdir -p $(PG_DIR) $(POSTGRES_DIR)

fix-perms:
	sudo chown -R $(PG_UID):$(PG_GID) $(PG_DIR)

shell:
	docker exec -it app bash
