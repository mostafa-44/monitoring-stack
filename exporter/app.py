import csv
import time
import os
from prometheus_client import start_http_server, Gauge, Counter, Summary
from collections import defaultdict

# ── Metric definitions ──────────────────────────────────────────────────────
total_revenue = Gauge(
    "sales_total_revenue",
    "Total revenue per product and region",
    ["product", "region", "category"]
)
total_units_sold = Gauge(
    "sales_total_units_sold",
    "Total units sold per product and region",
    ["product", "region", "category"]
)
total_profit = Gauge(
    "sales_total_profit",
    "Total profit per product and region",
    ["product", "region", "category"]
)
total_cost = Gauge(
    "sales_total_cost",
    "Total cost per product and region",
    ["product", "region", "category"]
)
profit_margin_pct = Gauge(
    "sales_profit_margin_percent",
    "Profit margin percentage per product",
    ["product", "category"]
)
records_processed = Counter(
    "csv_records_processed_total",
    "Total number of CSV records processed"
)
last_update = Gauge(
    "csv_last_update_timestamp",
    "Unix timestamp of the last CSV reload"
)
load_duration = Summary(
    "csv_load_duration_seconds",
    "Time taken to load and process the CSV file"
)

CSV_PATH = os.environ.get("CSV_PATH", "/data/sales_data.csv")
REFRESH_INTERVAL = int(os.environ.get("REFRESH_INTERVAL", "30"))


@load_duration.time()
def load_csv_metrics():
    """Read CSV and update all Prometheus metrics."""
    agg_revenue  = defaultdict(float)
    agg_units    = defaultdict(float)
    agg_profit   = defaultdict(float)
    agg_cost     = defaultdict(float)
    cat_map      = {}          # (product, region) -> category

    try:
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row["product"], row["region"])
                cat  = row["category"]
                cat_map[key] = cat

                agg_revenue[key] += float(row["revenue"])
                agg_units[key]   += float(row["units_sold"])
                agg_profit[key]  += float(row["profit"])
                agg_cost[key]    += float(row["cost"])
                records_processed.inc()

        # Push aggregated values to Prometheus
        for (product, region), rev in agg_revenue.items():
            cat = cat_map[(product, region)]
            total_revenue.labels(product=product, region=region, category=cat).set(rev)
            total_units_sold.labels(product=product, region=region, category=cat).set(agg_units[(product, region)])
            total_profit.labels(product=product, region=region, category=cat).set(agg_profit[(product, region)])
            total_cost.labels(product=product, region=region, category=cat).set(agg_cost[(product, region)])

        # Profit margin per product (across all regions)
        prod_revenue = defaultdict(float)
        prod_profit  = defaultdict(float)
        prod_cat     = {}
        for (product, region), rev in agg_revenue.items():
            prod_revenue[product] += rev
            prod_profit[product]  += agg_profit[(product, region)]
            prod_cat[product]      = cat_map[(product, region)]

        for product, rev in prod_revenue.items():
            margin = (prod_profit[product] / rev * 100) if rev > 0 else 0
            profit_margin_pct.labels(product=product, category=prod_cat[product]).set(margin)

        last_update.set(time.time())
        print(f"[{time.strftime('%H:%M:%S')}] ✅ Metrics updated — {len(agg_revenue)} label-sets loaded")

    except FileNotFoundError:
        print(f"[ERROR] CSV file not found: {CSV_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")


if __name__ == "__main__":
    PORT = int(os.environ.get("EXPORTER_PORT", "8000"))
    print(f"🚀 CSV Exporter starting on port {PORT}  (CSV: {CSV_PATH})")
    start_http_server(PORT)

    while True:
        load_csv_metrics()
        time.sleep(REFRESH_INTERVAL)
