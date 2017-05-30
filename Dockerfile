FROM ubuntu:14.04
MAINTAINER Bradley Griffiths <bradley.grififths@gmail.com>

RUN apt-get update -qq
RUN apt-get install -y python3-dev python3-crypto python3-pip python3-imaging
RUN apt-get install -y libpq-dev libjpeg-dev

RUN sudo pip install -U googlemaps
RUN sudo pip install flask-restful
RUN sudo pip3 install pillow

CMD 
