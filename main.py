from flask import Flask
from flask_mqtt import Mqtt
import json
from datetime import datetime
import pytz

tw = pytz.timezone('Asia/Taipei')

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'iot.sinew.com.tw'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0
mqtt = Mqtt(app)
timestamp_string = "2024-04-27 14:39:45"
format_string = "%Y-%m-%d %H:%M:%S"
connect_flag = False

@app.route('/')
def index():
    return 'hello world'

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    global connect_flag
    if not connect_flag and rc == 0:
    #if rc == 0:
        print("Connected to MQTT broker")
        mqtt.subscribe('elec110')
        connect_flag = True
    #else:
    #    print("Connection failed")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic=message.topic
    payload=message.payload.decode()
    power = json.loads(payload)
    #print (topic)
    if topic == 'elec110' :
        timestamp = power['ts']
        #print(type(timestamp))
        #datetime_object = datetime.strptime(str(power['ts']), format_string)
        #print(datetime_object)
        #dt_obj = datetime.fromtimestamp(timestamp)
        #print('Date Time:',dt_obj)
        #dt = datetime.datetime.strptime(dt_obj, '%Y-%m-%d %H:%M').replace(tzinfo=tw)
        dt = datetime.utcfromtimestamp(timestamp)
        print(dt)
        print('hello')
        #print(payload)

if __name__ == '__main__':
    app.run(debug=True)