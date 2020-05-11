FROM python:3.7

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip \
    && wget https://lilypond.org/download/binaries/linux-64/lilypond-2.20.0-1.linux-64.sh \
    && sh lilypond-2.20.0-1.linux-64.sh \
    && sudo apt-get install nginx \
    && pip install --no-cache-dir -r requirements.txt

