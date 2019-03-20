FROM balenalib/raspberrypi3-debian:stretch

RUN [ "cross-build-start" ]

# install deps
RUN sudo apt-get update
RUN sudo apt-get -y install python-dev python-setuptools libjpeg-dev python-cryptography python-imaging build-essential
RUN sudo mkdir /opt/ishiki
COPY requirements.txt /opt/ishiki/requirements.txt
WORKDIR /opt/ishiki
RUN sudo pip install -r requirements.txt

# install code
COPY deskcontrol /opt/ishiki/deskcontrol

CMD ["python", "-u", "deskcontrol/controller.py"]

RUN [ "cross-build-end" ]