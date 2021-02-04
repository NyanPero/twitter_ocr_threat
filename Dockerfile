FROM python:3.8-slim
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app

COPY requirements.txt /app

RUN apt update -y && \
    apt install git -y && \
    apt install libopencv-dev -y && \
    apt install whois -y && \
    apt install tesseract-ocr-jpn -y && \
    pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY /src /app
