FROM arupiot/ishiki-base:latest

RUN [ "cross-build-start" ]

WORKDIR /opt/ishiki

# install code
COPY deskcontrol /opt/ishiki/deskcontrol

CMD ["python", "-u", "deskcontrol/controller.py"]

RUN [ "cross-build-end" ]
