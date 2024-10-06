FROM python:3.12-alpine
RUN python3 -m pip install watchdog --no-cache-dir

# install kubectl
RUN apk add curl openssl bash --no-cache
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin

WORKDIR /app
COPY monitor.py /app
ENTRYPOINT ["python3", "-u", "monitor.py"]