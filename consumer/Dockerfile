FROM python:3.11.9


RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt update -y
RUN apt install -y chromium chromium-driver

RUN mkdir -p /opt/redis-consumer

COPY redis-consumer /opt/redis-consumer

WORKDIR /opt/redis-consumer

RUN pip install -r requirements.txt

CMD ["python", "-u", "redis-consumer.py"]