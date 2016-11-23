# -*- coding: utf-8- -*-

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json
import ssl, sys

pins = {37, 38}

def gpio_setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def gpio_destroy():
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
        GPIO.setup(pin, GPIO.IN)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("gpio")
    
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid))
   
def on_message(client, userdata, msg):
    print(" Payload: " + str(msg.payload))

    gpio = json.loads(str(msg.payload))

    if gpio['pin'] in pins:
        if gpio['value'] == 0:
            GPIO.output(gpio['pin'], GPIO.LOW)
            print ("LED turn off success")
        else:
            GPIO.output(gpio['pin'], GPIO.HIGH)
            print ("LED turn on success")

def on_disconnect():
    if rc != 0:
        print("Unexpected disconnection")
        
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.tls_set(ca_certs="/home/pi/CA/ca.crt",
                   certfile="/home/pi/CA/client.crt",
                   keyfile="/home/pi/CA/client.key",
                   tls_version=ssl.PROTOCOL_TLSv1_2)
    client.username_pw_set("user1", "rasp123")    
    gpio_setup()

    try:
        client.connect("192.168.1.103", port=8883)
        client.loop_forever()
    except KeyboardInterrupt:
        pass
    
    client.disconnect()
    gpio_destroy()
