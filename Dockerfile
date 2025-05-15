FROM python:3.11-slim
RUN pip install --no-cache-dir prometheus_client pyyaml
COPY run /etc
RUN chmod +x /etc/run
WORKDIR /app
COPY check.py .
COPY config.yaml .
STOPSIGNAL SIGKILL
ENTRYPOINT ["dumb-init", "--", "/etc/run"]