import asyncio, os
from app import logger
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2
from app.conf.config import url, number, topic
import json

class mqtt:
    def __init__(self, url = url, topic = topic, client_id=str(number)):
        self.client = MQTTClient(client_id=client_id)
        self.number = number
        self.topic = topic
        self.sub_topic = "$SYS/{}".format(str(number))
        self.url = url
        self.connected = False

    
    async def connect(self):
        await self.client.connect(self.url, cafile=os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'conf', 'server_cert.pem'))
        logger.info('client connected')
        self.connected = True

    async def subscribe(self):
        if not self.connected:
            await self.connect()
        await self.client.subscribe([(self.sub_topic, QOS_1),])

    async def publish(self, message):
        if not self.connected:
            await self.connect()
        await self.client.publish(self.topic, bytes(json.dumps(message), 'utf-8'))
        await self.disconnect()

    async def wait_for_message(self):
        message = await self.client.deliver_message()
        packet = message.publish_packet
        logger.info("{} => {}".format(packet.variable_header.topic_name, str(packet.payload.data)))
        return json.loads(bytes(packet.payload.data).decode())
    
    async def disconnect(self):
        await self.client.disconnect()
        self.connected = False
