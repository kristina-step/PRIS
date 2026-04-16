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
│ ├── app.py # Flask-приложение
│ └── Dockerfile # Docker образ
├── deployment.yaml # Kubernetes Deployment
├── service.yaml # Kubernetes Service
└── README.md # Эта инструкция
