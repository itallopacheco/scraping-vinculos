FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/


RUN apt-get update && apt-get upgrade -y


EXPOSE 8080

CMD ["python", "manage.py", "runserver","0.0.0.0:8080"]