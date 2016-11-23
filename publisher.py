# -*- coding: utf-8- -*-

import paho.mqtt.client as mqtt
import json
import ssl, sys, time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_publish(client, userdata, mid):
    print("mid: " + str(mid))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("unexptected disconnection")
        
def connect(i, flag):
    client.connect("192.168.1.103", port=8883)
    payload = '{\"pin\": ' + str(i) + ',\"value\": ' + str(flag) + '}'
    print (payload)
    client.publish("gpio", payload)
    client.disconnect()
    
    

if __name__ == '__main__':   
    client = mqtt.Client(client_id="test")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.tls_set(ca_certs="/home/pi/ca.crt",
                   certfile="/home/pi/server.crt",
                   keyfile="/home/pi/server.key",
                   tls_version=ssl.PROTOCOL_TLSv1_2)
    client.username_pw_set("client", "olsen307")
    n = -1
    flag = 1
    client.connect("192.168.1.103", port=8883)
    try:
        while (n < 0):
            if flag == 1:
                for i in [11, 15, 16, 18, 22]:
                    connect(i, flag)
                    time.sleep(3)
                flag = 0
            else:
                for i in [22, 18, 16, 15, 11]:
                    connect(i, flag)
                    time.sleep(3)
                flag = 1
                
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    
    client.disconnect()
