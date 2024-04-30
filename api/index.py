from flask import Flask
from flask_mqtt import Mqtt
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = os.getenv("MQTT_BROKER")
#app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0
app.config['MQTT_CLEAN_SESSION']= False
app.config['MQTT_KEEPALIVE'] = 5
mqtt = Mqtt(app)

timestamp_string = "2024-04-27 14:39:45"
format_string = "%Y-%m-%d %H:%M:%S"
connect_flag = False
last_message = None  # 用於存儲最後處理的訊息
pw = {}
@app.route('/')
def index():
    return 'hello world'

@app.route('/power')
def show_power():
    return pw

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    global connect_flag
    #print("Connected to MQTT broker")
    #mqtt.subscribe('elec110')
    #if not connect_flag and rc == 0:

    if rc == 0:
        print("Connected to MQTT broker")
        if not connect_flag:
            mqtt.subscribe('elec110')
            connect_flag = True
    else:
        print("Connection failed")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global last_message
    topic=message.topic
    payload=message.payload.decode()
    if payload != last_message:  # 確保不處理重複的訊息
        power = json.loads(payload)
        #print (topic)
        if topic == 'elec110' :
            global pw
            pw= power
            timestamp = power['ts']
            dt = datetime.utcfromtimestamp(timestamp)
            print(dt)
            print(pw)
            #print('hello')
            #print(payload)
        last_message = payload

@mqtt.on_disconnect()
def handle_disconnect(client, userdata, rc):
    global connect_flag
    connect_flag = False  # 斷開連線時重置連線狀態

'''
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)
'''

if __name__ == '__main__':
    app.run(use_reloader=False,debug=True)
