# IoT Desk Controller
Code to provide local controls for the Arup IoT desk. Utilises the tinkerforge hardware stack.

## Hardware
Intended to run on a tinkerforge redbrick but can run anywhere so long as you can connect to the tinkerforge stack over a network.

Will auto-detect bricklets compatible with the code and provide sensor readings / control of relays on a 128x64 OLED - joystick or multitouch can be used to navigate the menu.

VA_POSITIONS and RELAY_POSITIONS in config.py define which Voltage/Current bricklet and relay gets assigned to which label in the menu:

Voltage/Current Assignment:
* Port A: Laptop Charger Power (two of the 12V sockets)
* Port B: Monitor Power (the other 12V socket)
* Port C: USB Sockets (external facing only)
* Port D: Lighting

Relay Assignment:
* Port A: 1- Laptop Charger, 2- Monitor
* Port B: 1- USB Sockets, 2- Lighting

## Installation
Testing:
Start with ./python controller.py

Installation on Redbrick / Debian Jessie:
```
sudo cp deskcontrol /etc/init.d/deskcontrol
sudo update-rc.d deskcontrol defaults
sudo service deskcontrol start
```

## ToDo
* Add menu items to disable/change motion detection timer (currently 10 mins)
* Implement lighting control functionality (protocol tbc)

## History
March 2017 - First Revision
## Credits
Ben Hussey <ben.hussey@arup.com>
