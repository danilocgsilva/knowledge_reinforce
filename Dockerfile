FROM debian:bookworm-slim

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install git -y
RUN pip3 install SQLAlchemy Alembic pymysql mysql-connector-python python-dotenv flake8 black --break-system-packages

CMD while : ; do sleep 1000; done