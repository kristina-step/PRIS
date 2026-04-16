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
