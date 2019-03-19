FROM balenalib/raspberrypi3-debian:stretch

RUN [ "cross-build-start" ]

# install deps
RUN apt -y install python-dev python-setuptools libjpeg-dev python-cryptography
RUN sudo mkdir /opt/ishiki
COPY requirements.txt /opt/ishiki/requirements.txt
RUN sudo pip install -r requirements.txt

# install code
COPY deskcontrol /opt/ishiki/deskcontrol

WORKDIR /opt/ishiki

CMD ["python", "-u", "deskcontrol/controller.py"]

RUN [ "cross-build-end" ]