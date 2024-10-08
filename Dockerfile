FROM python:3.12.4


ENV DockerHome=/home/app/webapp

WORKDIR ${DockerHome}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

COPY . .
