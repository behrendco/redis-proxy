help: # Show help for Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

build: # Build or rebuild service.
	docker compose build

run: # Create and start containers.
	docker compose up -d

stop: # Stop and remove containers, networks.
	docker compose down

test-flask: # Execute HTTP web service tests.
	docker compose exec flask python3 -m pytest tests/

test-socket-server: # Execute Redis client protocol tests.
	docker compose exec socket_server python3 -m pytest tests/

test: # Build code and execute end-to-end tests.
	make build && make run && make test-flask && make test-socket-server && make stop

restart: # Stop, rebuild, restart containers.
	make stop && make build && make run