FROM python:3.7-slim-buster

WORKDIR /usr/src/app
COPY . ./

COPY ./config/api.conf /root/.config/api.conf
COPY ./scripts/download_models.sh /usr/local/bin/

# Installing dependencies
RUN apt-get update && \
    apt-get install -y -q python3-dev \
    gcc \
    build-essential \
    bash 

RUN make install

ENV PATH=/usr/src/app/.api-venv/bin:$PATH

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]
