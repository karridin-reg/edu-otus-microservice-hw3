## Общая информация

### Ingress controller
В качестве ингресс контроллера используется nginx, установлен в неймспейс `ingress-nginx`

## Разворачиваем приложения

### Основное приложение
Собрать Docker-образ:

```shell
docker build -t karridin/homework-5:1.0 -f ./deploy/docker/Dockerfile_main_app .
```

Залить образ в registry:

```shell
docker push karridin/homework-5:1.0
```

Развернуть базу данных:

```shell
kubectl apply -f deploy/k8s/0_database/*
```

Развернуть основное приложение:

```shell
kubectl apply -f deploy/k8s/1_main_app/*
```

### Сервис аутентификации
Предоставляет возможности для входа пользователя и генерирует JWT.
- Запросы к `/auth/*` попадают на `auth-service` и не проходят проверку авторизации
- Запросы к `/signup` попадают на `maip-app` и не проходят проверку авторизации
- Остальные запросы попадают на `maip-app` и проходят проверку авторизации


Собрать Docker-образ:

```shell
docker build -t auth-service:latest -f deploy/docker/Dockerfile_auth_service .
```

Развернуть в Kubernetes:

```shell
kubectl apply -f deploy/k8s/2_auth_service/*
```
