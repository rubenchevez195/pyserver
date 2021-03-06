FROM python:3.6


RUN git clone https://github.com/rubenchevez195/pyserver

RUN apt-get update -qq
RUN apt-get install -y python3-dev python3-crypto python3-pip python3-pil
RUN apt-get install -y libpq-dev libjpeg-dev

RUN pip install -U googlemaps
RUN pip install flask-restful
RUN pip3 install pillow

EXPOSE 8080


CMD cd pyserver && python pyserver.py

