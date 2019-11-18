# Dockerfile
FROM python:3.7

ADD . /app
WORKDIR /app
RUN pip install .

RUN mkdir -p /app/bin
RUN mkdir -p /app/bin/archives
ENV BASE_DIR /app/bin
RUN ls /app/bin

CMD ["python", "crawl"]