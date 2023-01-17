FROM python:3.9-slim-buster
	
RUN apt update && apt upgrade -y
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN pip3 install -U -r requirements.txt
CMD python3 notenews/__main__.py
