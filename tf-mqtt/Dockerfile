FROM arupiot/ishiki-base:mini

RUN [ "cross-build-start" ]

WORKDIR /opt/ishiki

# Get a verified version of the tinkerforge Python bindings
RUN apt-get install unzip
RUN wget https://download.tinkerforge.com/bindings/mqtt/tinkerforge_mqtt_bindings_2_0_7.zip
RUN unzip -j "tinkerforge_mqtt_bindings_2_0_7.zip" "tinkerforge_mqtt" -d .

CMD ["python", "-u", "tinkerforge_mqtt", "--debug", "--broker-host", "$BROKER_IP"]

RUN [ "cross-build-end" ]