FROM python:3.12.4-slim-bullseye@sha256:26ce493641ad3b1c8a6202117c31340c7bbb2dc126f1aeee8ea3972730a81dc6


RUN pip install uv
    

RUN uv venv /opt/venv

ENV PATH=/opt/venv/bin:$PATH

RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

COPY ./src /app

RUN uv pip install -r /tmp/requirements.txt

COPY ./boot/docker-run.sh /opt/run.sh

RUN chmod +x /opt/run.sh

RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD [ "/opt/run.sh" ]