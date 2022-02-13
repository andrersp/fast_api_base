FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./requirements.txt /app

RUN apt-get update && apt-get install libpq-dev gcc  -y
ENV TZ="America/Sao_Paulo"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install pip --upgrade
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

CMD ["gunicorn", "-w", "2", "--bind", ":8000", "{{cookiecutter.ms_name}}.app:create_app()", "--worker-class", "uvicorn.workers.UvicornWorker"]