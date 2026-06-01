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
<img width="1249" height="620" alt="image" src="https://github.com/user-attachments/assets/344b2a32-26f8-4e86-94f0-d0ed05293ba9" />


### 4. Доступ к приложению

```bash
# Проброс портов
kubectl port-forward service/my-app-service 5000:5000 &

# Или через Minikube
minikube service my-app-service --url
```
<img width="1545" height="861" alt="image" src="https://github.com/user-attachments/assets/40c2c29f-772b-4900-9083-850849c76689" />

<img width="1247" height="732" alt="image" src="https://github.com/user-attachments/assets/de350965-1bfb-424c-80b0-5984bc6ef009" />


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
<img width="1546" height="806" alt="image" src="https://github.com/user-attachments/assets/99516d76-3195-4064-b8c1-174c04e0ecb2" />


### 6. Настройка Horizontal Pod Autoscaler (HPA)

```bash
# Создание HPA (масштабирование при CPU > 50%)
kubectl autoscale deployment my-app --cpu-percent=50 --min=2 --max=5

# Проверка
kubectl get hpa
```

<img width="1536" height="614" alt="image" src="https://github.com/user-attachments/assets/ddb2e20d-15cb-4dde-b097-e5c05d61bac4" />


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

<img width="1535" height="800" alt="image" src="https://github.com/user-attachments/assets/785cf4d7-44af-40a6-81e6-3310baf89af6" />


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
<img width="880" height="497" alt="image" src="https://github.com/user-attachments/assets/8143212b-1dd1-4d9e-809e-ae34cd857869" />


<img width="1520" height="752" alt="image" src="https://github.com/user-attachments/assets/a27c70ca-676a-457a-9fb7-a16d1fd2f29d" />


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
<img width="1547" height="744" alt="image" src="https://github.com/user-attachments/assets/9300c63c-9a8c-459f-b44d-99bea6487390" />
<img width="1174" height="455" alt="image" src="https://github.com/user-attachments/assets/3a8ac73b-2ace-4acc-918f-3af2bc79d40c" />


## Результаты работы

<img width="1174" height="585" alt="image" src="https://github.com/user-attachments/assets/eb2b6b81-15ae-4a1e-ac9a-ae6a5b4fe876" />


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

### Демонстрация работы (записывали с другого устройства)
https://drive.google.com/file/d/1Wg7ZPp78V2cABvKnwXD_MKNjlwFG0L7_/view
