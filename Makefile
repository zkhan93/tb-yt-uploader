dev:
	docker-compose -f ./docker/docker-compose.dev.yml up --remove-orphans
dev-new:
	docker-compose -f ./docker/docker-compose.dev.yml up --remove-orphans
dev-update:
	docker-compose -f ./docker/docker-compose.dev.yml up --build -V --remove-orphans
