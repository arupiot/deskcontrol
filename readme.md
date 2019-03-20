# IoT Desk Controller
Code to provide local controls for the Arup IoT desk. Utilises the tinkerforge hardware stack.

## Hardware
Intended to run on a tinkerforge redbrick and Raspberry Pi but can run on any system with the required python dependencies installed so long as you can connect to the tinkerforge stack over a network.

It will auto-detect bricklets compatible with the code and provide sensor readings / control of relays on a 128x64 OLED - joystick or multitouch can be used to navigate the menu.

The code may need running multiple times before it runs successfully.

## Installation
Requirements for Debian based systems:
```
sudo apt-get install libusb-1.0-0 libudev0 pm-utils
wget http://download.tinkerforge.com/tools/brickd/linux/brickd_linux_latest_armhf.deb
sudo dpkg -i brickd_linux_latest_armhf.deb
apt-get install python-dev python-setuptools libjpeg-dev python-cryptography 
pip install -r requirements.txt
```


Testing mode:
```
./python controller.py
```

Installation on Redbrick / Debian Jessie:
```
sudo cp deskcontrol.init /etc/init.d/deskcontrol
sudo update-rc.d deskcontrol defaults
sudo service deskcontrol start
```

## ToDo
* Add menu items to disable/change motion detection timer (currently 10 mins)
* Implement lighting control functionality (protocol tbc)
* Add touch interface using KiVi on WaveShare 3.5" touch screen for Raspberry Pi
* Add microphone based sound sensor

## Credits
* Ben Hussey <ben.hussey@arup.com>
* Francesco Anselmo <francesco.anselmo@arup.com>
* George Ogden <2287@trinity.croydon.sch.uk>

