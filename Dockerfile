FROM python:3.7.3

WORKDIR /data

RUN apt-get update && apt-get install -y \
    gcc \
    musl-dev \
    build-essential \
    libpq-dev \
    libffi-dev \
    openssl \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /data/requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD tail -f /dev/null
