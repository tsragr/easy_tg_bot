FROM python:3.8

RUN mkdir -p /tg_bot
WORKDIR /tg_bot
ADD . .
RUN apt-get update && apt-get install -y gcc python3-dev locales locales-all gettext libmagic-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt

CMD python tg_bot.py