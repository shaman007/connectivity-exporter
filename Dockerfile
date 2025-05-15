FROM python:3.11-slim
RUN apt-get update && apt-get upgrade -y && apt-get install dumb-init -y && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install --no-cache-dir prometheus_client pyyaml
COPY run /etc
RUN chmod +x /etc/run
WORKDIR /app
COPY check.py .
COPY config.yaml .
STOPSIGNAL SIGKILL
ENTRYPOINT ["dumb-init", "--", "/etc/run"]