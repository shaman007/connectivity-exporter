# connectivity-exporter

Inspired by this post: [https://antonz.org/is-online/](https://antonz.org/is-online/)

Prometheus compatible exporter that checks connectivity to given HTTP URI. Default config.yaml checks public internet services, however, you can use it to check API status of your own applications. Don't abuse public services!

## Usage

Sample config:

```yaml
endpoints:
  - url: https://google.com/generate_204
    expect: 204
  - url: http://captive.apple.com/hotspot-detect.html
    expect: 200
```

and then use it:

```bash
python check.py --config config.yaml --port 9000 --interval 60
```

Or via environment:

```bash
export CONFIG=config.yaml
export PORT=9000
export INTERVAL=30
python check.py
```

then scrape:

```yaml
- job_name: 'connectivity-exporter'
  static_configs:
    - targets: ['connectivity-exporter.default.svc.cluster.local:8443']

```

## Deployment

Sample Dokerfile and K8S deployment are provided

## ToDo

Fancy hompage that shows current situation.
