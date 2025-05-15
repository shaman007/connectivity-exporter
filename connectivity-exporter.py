import os
import time
import threading
import argparse
import http.client
import datetime as dt
from urllib.parse import urlparse
import yaml
from prometheus_client import start_http_server, Gauge

DEFAULT_INTERVAL = 45
DEFAULT_PORT = 8443

# Prometheus metrics
status_gauge = Gauge('connectivity_status', 'Connection status (1=OK, 0=Fail)', ['host'])
time_gauge = Gauge('connectivity_time_ms', 'Response time in milliseconds', ['host'])

def check_endpoint(url: str, expected_status: int, timeout: dt.timedelta = dt.timedelta(seconds=1)):
    parsed = urlparse(url)
    host = parsed.netloc
    start = time.perf_counter()
    try:
        conn_class = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
        conn = conn_class(host, timeout=timeout.total_seconds())
        conn.request("GET", parsed.path or "/")
        response = conn.getresponse()
        status_code = response.status
        success = (status_code == expected_status)
    except Exception:
        status_code = -1
        success = False
    finally:
        try:
            conn.close()
        except:
            pass
    elapsed_ms = (time.perf_counter() - start) * 1000
    return host, status_code, success, elapsed_ms

def check_loop(endpoints: list, interval: int):
    while True:
        for entry in endpoints:
            url = entry["url"]
            expected = entry.get("expect", 204)
            host, actual, ok, duration = check_endpoint(url, expected)
            print(f"{host} -> {'✅' if ok else f'❌ ({actual})'} (expected {expected}, {duration:.2f} ms)")
            status_gauge.labels(host=host).set(1 if ok else 0)
            time_gauge.labels(host=host).set(duration)
        time.sleep(interval)

def load_config(path: str):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def resolve_option(cli_val, env_var, default_val, cast_func=str):
    env_val = os.getenv(env_var)
    if cli_val is not None:
        return cli_val
    elif env_val is not None:
        return cast_func(env_val)
    else:
        return default_val

def main():
    parser = argparse.ArgumentParser(description="Connectivity checker with Prometheus metrics.")
    parser.add_argument("--port", type=int, help="Port to serve /metrics on (env: PORT)")
    parser.add_argument("--interval", type=int, help="Interval in seconds between checks (env: INTERVAL)")
    parser.add_argument("--config", type=str, help="Path to YAML config file (env: CONFIG)")

    args = parser.parse_args()

    port = resolve_option(args.port, "PORT", DEFAULT_PORT, int)
    interval = resolve_option(args.interval, "INTERVAL", DEFAULT_INTERVAL, int)
    config_path = resolve_option(args.config, "CONFIG", None)

    if not config_path:
        print("❌ No config file specified via --config or CONFIG env variable.")
        exit(1)

    try:
        config = load_config(config_path)
        endpoints = config.get("endpoints", [])
        if not endpoints:
            raise ValueError("No endpoints defined in config")
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        exit(1)

    print(f"✅ Starting HTTP server on port {port} and checking every {interval}s")
    start_http_server(port)

    thread = threading.Thread(target=check_loop, args=(endpoints, interval), daemon=True)
    thread.start()

    while True:
        time.sleep(3600)

if __name__ == "__main__":
    main()
