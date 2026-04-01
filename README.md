# 📊 Monitoring Stack (Prometheus + Grafana + ELK)

## 📌 Overview

This project is a complete monitoring stack built using open-source tools.
It helps track system performance, container metrics, and logs in one place.

The idea is simple: collect data → process it → visualize it.

---

## 🧱 Architecture

Metrics:
Node Exporter / cAdvisor → Prometheus → Grafana

Logs:
Filebeat → Logstash → Elasticsearch → Kibana

---

## ⚙️ Tools Used

- Prometheus → collect metrics
- Grafana → dashboards
- Elasticsearch → store logs
- Logstash → process logs
- Kibana → view logs
- cAdvisor → container metrics
- Node Exporter → system metrics
- Docker Compose → run everything

---

## 🚀 How to Run

Clone the repo:

```bash id="a1b2c3"
git clone https://github.com/mostafa-44/monitoring-stack.git
cd monitoring-stack
```

Run the stack:

```bash id="d4e5f6"
docker compose up -d
```

---

## 🌐 Access

- Grafana → http://localhost:3000
- Prometheus → http://localhost:9090
- Kibana → http://localhost:5601

---

## 📊 What You Can Monitor

- CPU / Memory usage
- Docker containers
- Logs and errors
- System performance

---

## 📸 Screenshots

### Grafana Dashboard

![dashboard](image.png)

### Prometheus Queries

![alt text](image-1.png)

### Architecture

![alt text](image-2.png)

---

## 💡 Notes

- The stack runs بالكامل باستخدام Docker
- Easy to start with one command
- Can be extended لأي system أو application

---

## 🔧 Future Improvements

- Add alerts using Alertmanager
- Move to Kubernetes
- Add real application monitoring

---

## 👤 Author

Mostafa Atef
