#!/usr/bin/python

import paho.mqtt.client as mqtt
import motephat as mote
import simplejson as json
from time import sleep
import sys

# Keep lights on if script exits
mote.set_clear_on_exit(False)

# Helpers
def hex_to_dec(hex):
    return list(int(hex[i:i+2], 16) for i in range(0,len(hex),2))

# Handle command
def handleRequest(req):
    
    #print (req)

    # Clear cmd
    if req['cmd'] == 'clear' or req['cmd'] == 'clr' or req['cmd'] == 'cls':
        if 'channel' in req:
            if type(req['channel']) is list:
                for channel in req['channel']:
                    mote.clear_channel(channel)
            else:
                mote.clear_channel(req['channel'])
        elif 'channels' in req and type(req['channels']) is list:
            for channel in req['channels']:
                mote.clear_channel(channel)
        else:
            mote.clear()

    # Brightness cmd
    if req['cmd'] == 'brightness':
        mote.set_brightness(req['brightness'])

    # Fill one or more pixels
    if req['cmd'] == 'fill':

        # Seutp vars
        channels = []
        pixels = []
        colors = []

        # Parse request args
        if 'channel' in req:
            if type(req['channel']) is list:
                channels.extend(req['channel'])
            else:
                channels.append(req['channel'])
        elif 'channels' in req and type(req['channels']) is list:
            channels.extend(req['channels'])

        if 'pixel' in req:
            if type(req['pixel']) is list:
                pixels.extend(req['pixel'])
            else:
                pixels.append(req['pixel'])
        elif 'pixels' in req and type(req['pixels']) is list:
            pixels.extend(req['pixels'])

        if 'color' in req:
            if type(req['color']) is list:
                colors.extend(req['color'])
            else:
                colors.append(req['color'])
        elif 'colors' in req and type(req['colors']) is list:
            colors.extend(req['colors'])

        # Validate values
        if len(channels) == 0:
            channels = list(range(0,4))
        
        if len(pixels) == 0:
            pixels = list(range(0,16))

        # Fill pixels
        cm = len(colors)
        for c in channels:
            ci = 0
            for p in pixels:

                color = colors[ci]
                rgb = [0,0,0]
                brightness = None

                if type(color) is list and (len(color) == 3 or len(color) == 4):
                    rgb = color
                elif type(color) is str and (len(color) == 6 or len(color) == 8):
                    rgb = hex_to_dec(color)
                
                if len(rgb) > 3:
                    brightness = rgb[3]/255.0
                    rgb = rgb[:3]

                mote.set_pixel(c+1,p,rgb[0],rgb[1],rgb[2],brightness)

                ci += 1
                if (ci >= cm):
                    ci = 0

        # Show the pixels
        mote.show()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print('Connected with result code '+ str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('pi/motephat')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print("Request received: " + str(msg.payload))
    req = json.loads(msg.payload)
    handleRequest(req)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('10.20.0.200', 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()