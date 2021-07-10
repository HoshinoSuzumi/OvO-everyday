FROM python:3.9.6-slim
MAINTAINER HoshinoSuzumi <rbq@ibox.moe>
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
VOLUME /ds/data

CMD [ "uvicorn", "--header", "server:ovo-powered", "--host", "0.0.0.0", "--port", "80", "main:app" ]