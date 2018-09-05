# motephat-mqtt

A Python MQTT client to control a Pimoroni MOTE pHAT

# Installation

Start by updating / upgrading your installation (Optional)

    sudo apt-get update
    sudo apt-get upgrade

Install the [motephat](https://github.com/pimoroni/mote-phat) library

    curl https://get.pimoroni.com/motephat | bash

Next, install other pre-requisit packages

    pip install paho-mqtt simplejson

Next, clone the motephat-mqtt repository (I'll assume to `/home/pi/`)

    git clone https://github.com/circuitbeard/motephat-mqtt.git

Next, update the IP address of the MQTT broker and the topic to connect to

    sudo nano motephat-mqtt/motephat-mqtt.py
    >>> client.subscribe('YOUR TOPIC')
    >>> client.connect('YOUR BROKER IP', 1883, 60)

Next, make sure `job.sh` is executable

    sudo chmod +x motephat-mqtt/job.sh

Next, setup a service to start once a network is available (taken from [here](https://raspberrypi.stackexchange.com/questions/78991/running-a-script-after-an-internet-connection-is-established))

````
sudo systemctl edit --force --full motephat-mqtt.service
````

````
[Unit]
Description=MOTE pHAT MQTT Service
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/pi/motephat-mqtt
ExecStart=/home/pi/motephat-mqtt/job.sh

[Install]
WantedBy=multi-user.target
````

````
sudo systemctl enable my_script.service
sudo systemctl start my_script.service
````

# Usage

The MQTT client supports several commands, all expressed through JSON payloads

## Clear

### Clear everything
````
{
    'cmd': 'clr'
}
````

### Clear a specific channel
````
{
    'cmd': 'clr',
    'channel': 0
}
````

### Clear several channels at once
````
{
    'cmd': 'clr',
    'channels': [0,3]
}
````