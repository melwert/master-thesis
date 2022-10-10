FROM python:3

RUN apt-get update && apt-get -y install cron

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY crontab /etc/cron.d/daily_scan
RUN chmod 0644 /etc/cron.d/daily_scan
RUN crontab /etc/cron.d/daily_scan

RUN chmod +x start.sh

#CMD [ "python", "./setup.py" ]

CMD /usr/src/app/start.sh && cron -f
