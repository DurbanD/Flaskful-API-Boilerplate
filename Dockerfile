FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y python3-pip python3-dev ufw

WORKDIR /app

COPY . .


RUN ufw allow 5000

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["app.py"]
