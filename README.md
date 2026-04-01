# 📊 Monitoring Stack — Data Engineering Course
### Prometheus · Grafana · CSV Exporter · Docker Compose

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Docker Network: monitoring                  │
│                                                                     │
│  ┌──────────────┐     scrape      ┌──────────────┐                 │
│  │              │  ──────────────▶│              │                 │
│  │  Prometheus  │  :9090          │ CSV Exporter │  :8000          │
│  │              │◀── /metrics ─── │  (Python)    │                 │
│  └──────┬───────┘                 └──────┬───────┘                 │
│         │ datasource                     │ reads                   │
│         ▼                                ▼                          │
│  ┌──────────────┐                ┌──────────────┐                 │
│  │   Grafana    │  :3000         │  sales_data  │                 │
│  │  Dashboards  │                │   .csv       │                 │
│  └──────────────┘                └──────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
monitoring-stack/
├── docker-compose.yml              ← Orchestrates all services
│
├── data/
│   └── sales_data.csv              ← Your CSV data source
│
├── exporter/
│   ├── Dockerfile                  ← Python 3.11 slim image
│   ├── requirements.txt            ← prometheus_client
│   └── app.py                      ← Reads CSV → exposes /metrics
│
├── prometheus/
│   └── prometheus.yml              ← Scrape config (15s interval)
│
└── grafana/
    ├── provisioning/
    │   ├── datasources/
    │   │   └── prometheus.yml      ← Auto-connects Prometheus
    │   └── dashboards/
    │       └── dashboards.yml      ← Tells Grafana where dashboards live
    └── dashboards/
        └── sales_dashboard.json    ← Pre-built sales dashboard
```

---

## 🚀 Quick Start

### Prerequisites
- Docker ≥ 24.x
- Docker Compose ≥ 2.x

### 1 — Clone / copy this folder, then:

```bash
cd monitoring-stack

# Build & start all containers (first run builds the exporter image)
docker compose up --build -d

# Watch logs (optional)
docker compose logs -f
```

### 2 — Access the UIs

| Service    | URL                        | Credentials       |
|------------|----------------------------|-------------------|
| Grafana    | http://localhost:3000      | admin / admin123  |
| Prometheus | http://localhost:9090      | —                 |
| Exporter   | http://localhost:8000/metrics | —              |

### 3 — Open Grafana
1. Go to **http://localhost:3000**
2. Login with `admin` / `admin123`
3. The **📊 Sales Data Monitoring** dashboard loads automatically

---

## 📈 Exposed Metrics

| Metric Name                        | Type    | Labels                          | Description                  |
|------------------------------------|---------|----------------------------------|------------------------------|
| `sales_total_revenue`              | Gauge   | product, region, category        | Total revenue                |
| `sales_total_units_sold`           | Gauge   | product, region, category        | Units sold                   |
| `sales_total_profit`               | Gauge   | product, region, category        | Total profit                 |
| `sales_total_cost`                 | Gauge   | product, region, category        | Total cost                   |
| `sales_profit_margin_percent`      | Gauge   | product, category                | Profit margin %              |
| `csv_records_processed_total`      | Counter | —                                | Total CSV rows processed     |
| `csv_last_update_timestamp`        | Gauge   | —                                | Unix timestamp of last reload|
| `csv_load_duration_seconds`        | Summary | —                                | CSV processing duration      |

---

## 🔍 Useful PromQL Queries (Prometheus UI)

```promql
# Total revenue across all products
sum(sales_total_revenue)

# Revenue broken down by product
sum by (product) (sales_total_revenue)

# Revenue broken down by region
sum by (region) (sales_total_revenue)

# Top product by profit
topk(3, sum by (product) (sales_total_profit))

# Profit margin per product
sales_profit_margin_percent

# How many times CSV was reloaded
rate(csv_records_processed_total[5m])
```

---

## ♻️ Updating the CSV Data

1. Edit `data/sales_data.csv` (add rows, change values)
2. The exporter **automatically reloads** every 30 seconds — no restart needed
3. Watch Prometheus pick up the new values within ~15 seconds

---

## 🛑 Stop & Clean Up

```bash
# Stop containers (keeps volumes)
docker compose down

# Stop AND remove all data volumes
docker compose down -v
```

---

## 🧪 Course Concepts Demonstrated

| Concept                         | Where                          |
|---------------------------------|--------------------------------|
| **Containerization**            | All services in Docker         |
| **Service Discovery**           | Docker DNS (service names)     |
| **Metrics Collection**          | Prometheus scraping exporter   |
| **Data Ingestion**              | CSV → Python → Prometheus      |
| **Time-Series Storage**         | Prometheus TSDB (7-day window) |
| **Visualization**               | Grafana dashboards             |
| **Health Checks**               | docker-compose healthcheck     |
| **Configuration as Code**       | All provisioned via YAML       |
| **Observability Pipeline**      | Exporter → Prometheus → Grafana|
