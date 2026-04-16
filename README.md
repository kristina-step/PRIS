# Лабораторная работа: Развертывание сервиса в Kubernetes (Minikube)

## Цель работы
Ознакомиться с Kubernetes, развернуть сервис с использованием Minikube, настроить автоматическое масштабирование (HPA) и систему мониторинга (Prometheus + Grafana).

## Студенты
- Кристина Степкина Владимировна
- Максимова Ольга Сергеевна
- Соколова Вера Павловна
- Клапнева Диана Дмитриевна

##  Используемые технологии
- **Kubernetes** (Minikube) – оркестрация контейнеров
- **Docker** – контейнеризация приложения
- **Python + Flask** – веб-приложение
- **Metrics Server** – сбор метрик CPU/памяти
- **Horizontal Pod Autoscaler (HPA)** – автоматическое масштабирование
- **Prometheus + Grafana** – мониторинг и визуализация
- **Helm** – пакетный менеджер для Kubernetes

---

## Структура репозитория

PRIS/

├── app/

│ ├── app.py 

│ └── Dockerfile 

├── deployment.yaml

├── service.yaml

└── README.md # 


---

##  Инструкция по развертыванию

### 1. Установка Minikube и запуск кластера

```bash
# Установка Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Запуск кластера
minikube start --driver=docker --cpus=2 --memory=4096

# Проверка
kubectl cluster-info
kubectl get nodes
```
### 2. Сборка Docker образа

```bash
# Переключение на Docker демон Minikube
eval $(minikube docker-env)

# Сборка образа
docker build -t my-app:latest app/

# Проверка
docker images | grep my-app
```

### 3. Развертывание приложения

```bash
# Применение конфигураций
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Проверка подов (должно быть 3)
kubectl get pods

# Проверка сервиса
kubectl get services
```

### 4. Доступ к приложению

```bash
# Проброс портов
kubectl port-forward service/my-app-service 5000:5000 &

# Или через Minikube
minikube service my-app-service --url
```

### 5. Установка Metrics Server

```bash
# Установка
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Патч для работы в Codespaces/Minikube
kubectl patch deployment metrics-server -n kube-system --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'

# Проверка
kubectl top nodes
kubectl top pods
```

### 6. Настройка Horizontal Pod Autoscaler (HPA)

```bash
# Создание HPA (масштабирование при CPU > 50%)
kubectl autoscale deployment my-app --cpu-percent=50 --min=2 --max=5

# Проверка
kubectl get hpa
```

### 7. Установка Prometheus и Grafana через Helm

```bash
# Установка Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Добавление репозитория
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Установка стека мониторинга
helm install prometheus prometheus-community/kube-prometheus-stack

# Проверка подов
kubectl get pods
```
### 8. Доступ к Grafana

```bash
# Получение пароля admin
kubectl get secret prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode

# Проброс порта
kubectl port-forward deployment/prometheus-grafana 3000:3000
```
Доступ в браузере: http://localhost:3000

Логин: admin

Пароль: (полученный выше)


### 8. Тестирование автомасштабирования

Терминал 1 (наблюдение):

```bash
kubectl get pods -w
```

Терминал 2 (нагрузка):

```bash
kubectl run -it --rm load-generator --image=busybox -- /bin/sh
# Внутри контейнера:
while true; do wget -q -O- http://my-app-service.default.svc.cluster.local:5000; done
```
## Результаты работы

### HPA в действии
```bash
NAME     REFERENCE           TARGETS    MINPODS   MAXPODS   REPLICAS
my-app   Deployment/my-app   cpu: 102%/50%   2         5         4
```

### Метрики подов
```bash
NAME                         CPU(cores)   MEMORY(bytes)
my-app-6c7747b8b6-f7pwb     85m          128Mi
my-app-6c7747b8b6-mg6pf     92m          130Mi
my-app-6c7747b8b6-qh64c     78m          125Mi
my-app-6c7747b8b6-qktgm     88m          129Mi
```

