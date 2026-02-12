# Dockerfile for running Galician TTS with phoneme preprocessing
# Prerequisite: download appropriate cotovia deb packages to <project-dir>/deb
# https://sourceforge.net/projects/cotovia/files/Debian%20packages/

FROM python:3.10-slim-bookworm

# Project setup

ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update \
    && apt-get install gcc g++ mecab libmecab-dev mecab-ipadic-utf8 libsndfile1 -y \
    && apt-get install libasound2 libc6 libgcc1 libstdc++6 -y \
    && apt-get install bison flex libfl-dev libasound2-dev libexpat1 libexpat1-dev -y\
    && apt-get install build-essential cmake make git -y \
    && apt-get clean

RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install  --quiet --upgrade pip && \
    pip install  --quiet pip-tools

RUN pip install spacy==3.7.5

COPY . /app

RUN dpkg -i /app/deb/cotovia-1.0.0.deb
#RUN dpkg -i /app/deb/cotovia-lang-gl_0.5_all.deb

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

#RUN cp /app/deb/gl/* /usr/share/cotovia/data/lang/gl/ #copy content of app/deb/gl to /usr/share/cotovia/data/lang/gl

# RUN ls /usr/share/cotovia/data/lang/gl

WORKDIR /app

ENV PYTHONUNBUFFERED=1
