FROM python
WORKDIR /
COPY projectchatbot.py /
COPY requirements.txt /
RUN pip install update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=5297721044:AAGaPVlkwFAUU9tPSw6DrCEGLWnHpzyT6bw
ENV HOSTREDIS=redis-11960.c57.us-east-1-4.ec2.cloud.redislabs.com
ENV PASSWORDREDIS=KgMUHovC84Y5qQ1NFmPGf1sEXtw7lRFF
ENV REDISPORT=11960
ENV HOSTSQL=124.71.41.226
ENV USERSQL=root
ENV DATABASESQL=chatbot
ENV PORTSQL=3306
ENV PASSWORDSQL=Hkbucloud!
CMD python projectchatbot.py

