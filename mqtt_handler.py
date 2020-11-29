import uuid
import paho.mqtt.client as mqtt
import mraa
import time

from os import environ, geteuid

from pixel_ring import pixel_ring
from utils import read_json, current_time


class MqttHandler:
    def __init__(self):
        # It's required to change GPIO state on Respeaker Core V2 before the actual LED processing.
        self.gpio = mraa.Gpio(12)
        if geteuid() != 0 :
            time.sleep(1)
        
        self.gpio.dir(mraa.DIR_OUT)
        self.gpio.write(0)

        # Change LED color preset. Google pattern is enabled by default. Echo stands for Amazon Echo Speaker.
        pixel_ring.change_pattern('echo')

        # Load MQTT settings.
        config = read_json("config")
        self.mqtt_address = config["mqttAddress"]
        self.mqtt_username = config["mqttUser"]
        self.mqtt_password = config["mqttPassword"]
        self.__init_mqtt_client()

    async def start(self):
        self.mqtt_client.connect(self.mqtt_address)
        task = await self.mqtt_client.loop_start()
        return task

    def send(self, topic, message):
        self.mqtt_client.publish(topic, message)

    def stop(self):
        # Restore GPIO state on exit.
        self.gpio.write(1)
        self.mqtt_client.loop_stop(True)
        print(current_time(), 'Disconnected from MQTT server.')

    def __init_mqtt_client(self):
        self.mqtt_client = mqtt.Client("RespeakerLED-" + uuid.uuid4().hex)
        self.mqtt_client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.mqtt_client.on_connect = self.__on_mqtt_connect
        self.mqtt_client.on_message = self.__on_mqtt_message

    def __on_mqtt_connect(self, client, obj, flags, rc):
        print(current_time(), 'Connected to MQTT server.')
        self.mqtt_client.subscribe('respeaker/led/#')

    def __on_mqtt_message(self, client, obj, msg):
        topic = msg.topic
        if topic.endswith('/wake'):
            angle = msg.payload.decode('utf-8')
            adjusted_angle = (int(angle) + 360 - 60) % 360
            pixel_ring.wakeup(adjusted_angle)
        elif topic.endswith('/listen'):
            pixel_ring.listen()
        elif topic.endswith('/speak'):
            pixel_ring.speak()
        elif topic.endswith('/think'):
            pixel_ring.think()
        elif topic.endswith('/sleep'):
            pixel_ring.off()
