.PHONY: help build up start down stop restart logs
build:
	docker-compose --env-file .env.dev -f docker-compose.yml build $(c)
up:
	docker-compose --env-file .env.dev -f docker-compose.yml up -d $(c)
start:
	docker-compose --env-file .env.dev -f docker-compose.yml start $(c)
down:
	docker-compose --env-file .env.dev -f docker-compose.yml down $(c)
stop:
	docker-compose --env-file .env.dev -f docker-compose.yml stop $(c)
restart:
	docker-compose --env-file .env.dev -f docker-compose.yml stop $(c)
	docker-compose --env-file .env.dev -f docker-compose.yml up -d $(c)
logs:
	docker-compose --env-file .env.dev -f docker-compose.yml logs --tail=100 -f $(c)
test:
	DJANGO_SU_EMAIL=pirojgok@gmail.com DJANGO_SU_PASSWORD=adminadmin123 pytest -vv ./api_handler/tests
