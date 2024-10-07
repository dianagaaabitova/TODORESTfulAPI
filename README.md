## Чтобы поднять локально:
````
docker compose up -d
````

## Поднять на сервере:
Чтобы поднять, нужно сначала удалить (1 строка)
````
docker-compose.override
docker network create traefik-public
docker compose up -d --build
docker compose -f docker-compose.traefik.yml up -d
````
SSL сертификат получится *автоматически*.

## Метрики:
http://grafana.localhost/d/3dkRGSYnk/fastapi?orgId=1&refresh=5s

Логин: admin

Пароль: admin

## Документация:
http://localhost/api/docs
