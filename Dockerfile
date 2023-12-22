FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN pip install --no-cach-dir -r requirements.txt

ARG PORT_NUMBER
ENV NGROK_PORT=$PORT_NUMBER
EXPOSE $NGROK_PORT

ENTRYPOINT [ "python", "./main.py", "-e", "PORT_NUMBER" ]
