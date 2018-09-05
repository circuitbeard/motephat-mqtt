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
Description=A MOTE pHAT MQTT Client Service
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
sudo systemctl enable motephat-mqtt.service
sudo systemctl start motephat-mqtt.service
````

# Usage

The MQTT client supports several commands, all expressed through JSON payloads

## Clear
Clear one, multiple or all channels

#### Clear everything
````
{
    'cmd': 'clear'
}
````

#### Clear a specific channel
````
{
    'cmd': 'clear',
    'channel': 0
}
````

#### Clear several channels at once
````
{
    'cmd': 'clear',
    'channels': [0,3]
}
````

## Brightness
Control the global brightness level

````
{
    'cmd': 'brightness',
    'brightness': 0.5
}
````

## Fill
Fill one, multiple or all pixels

#### Fill everything
````
{
    'cmd': 'fill',
    'color': 'FF0000'
}
````

#### Fill a specific channel
````
{
    'cmd': 'fill',
    'channel': 0,
    'color': 'FF0000'
}
````

#### Fill multiple channels
````
{
    'cmd': 'fill',
    'channels': [0,3],
    'color': 'FF0000'
}
````

#### Fill specific pixel
````
{
    'cmd': 'fill',
    'channel': 0,
    'pixel': 3,
    'color': 'FF0000'
}
````

#### Fill multiple pixels
````
{
    'cmd': 'fill',
    'channel': 0,
    'pixels': [0,2,5,7,9],
    'color': 'FF0000'
}
````

#### Fill multiple pixels in multiple channels
````
{
    'cmd': 'fill',
    'channels': [0,3],
    'pixels': [0,2,5,7,9],
    'color': 'FF0000'
}
````

#### Colours
For all fill commands, colours can be expressed in multiple ways

* **'FF0000'** - Standard hex
* **'FF0000CC'** - Hex + brightness
* **[255,0,0]** - Standard RGB
* **[255,0,0, 150]** - RGB + brightness

In addition to the colour formats, fill commands can also accept multiple colours at once (except where targeting a single pixel). 

````
{
    'cmd': 'fill',
    'channels': [0,3],
    'pixels': [0,2,5,7,9],
    'colors': ['FF0000','00FF00','0000FF']
}
````

When providing multiple colours, as each pixel is rendered in a channel, the pixel will take the colour at the pixels index in the colour list. If the colour list is shorter than the number of pixels, then the colours will be looped through mulitple times. So in the example above, the selected channels will have pixel colours:

    red, green, blue, red, green, blue, red...