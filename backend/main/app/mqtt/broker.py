import logging
import asyncio
import os
from hbmqtt.broker import Broker

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'max-connections': "1000",
            'bind': '0.0.0.0:8883',
            'ssl': 'on',
            'certfile': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ssl', 'server_cert.pem'),
            'keyfile':  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ssl','server_key.pem')
        },
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': False,
        'password-file': os.path.join(os.path.dirname(os.path.realpath(__file__)), "passwd"),
        'plugins': [
            'auth_file', 'auth_anonymous'
        ]

    }
}



async def coro(broker):
    await broker.start()


def start_broker(loop=asyncio.new_event_loop()):
    asyncio.set_event_loop(loop)
    broker = Broker(config)
    loop.run_until_complete(coro(broker))
    loop.run_forever()

if __name__ == "__main__":
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    start_broker()
