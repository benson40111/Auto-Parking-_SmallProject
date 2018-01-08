import asyncio
import os

from app import logger
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2
from app.conf.config import url
from app.modules import db, mail as Mail
from threading import Thread
from datetime import datetime, timezone, timedelta
import json

async def uptime_coro():
    client = MQTTClient()
    mail = Mail.mail()
    await client.connect(url, cafile=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ssl' ,'server_cert.pem'))
    await client.subscribe([
        ('$SYS/park', QOS_1),
        ])
    logger.info("Subscribed")
    try:
        while True:
            message = await client.deliver_message()
            packet = message.publish_packet
            print("{} => {}".format(packet.variable_header.topic_name, str(packet.payload.data)))
            try:
                data = json.loads(bytes(packet.payload.data).decode())
                method = data.get('method', False)
                number = data.get('number', 0)
                message = { 'error_request' : True }
                IOT = db.IOT.objects.get(number=number)
                topic = '$SYS/{}'.format(number)
                if method == 'GET':
                    IOT.is_online = True 
                    IOT.online_time = datetime.now()
                    message.update(json.loads(IOT.to_json()))
                    message['method'] = method
                    message['error_request'] = False
                    IOT.save()
                elif method == 'POST':
                    user = db.User.objects.get(rfid=data.get('rfid'))
                    if IOT.is_used and user.is_used and user.rfid == IOT.rfid:
                        IOT.is_used = False
                        user.is_used = False
                        message['locked'] = False
                        message['method'] = method
                        message['error_request'] = False
                    elif not IOT.is_used and not user.is_used:
                        user.is_used = True
                        IOT.is_used = True
                        user.last_time = datetime.now()
                        IOT.last_time = datetime.now()
                        user.last_address = IOT.address
                        user.last_number = IOT.number
                        user.usage_times += 1
                        IOT.usage_times += 1
                        IOT.rfid = user.rfid
                        IOT.last_user = user.email
                        message['locked'] = True
                        message['rfid'] = user.rfid
                        message['error_request'] = False
                        message['method'] = method
                    IOT.save()
                    user.save()

                elif method == 'ERROR':
                    user = db.User.objects.get(rfid=data.get('rfid'))
                    date = data.get('time', None)
                    if date == None:
                        dt = datetime.utcnow().replace(tzinfo=timezone.utc)
                        tzutc_8 = timezone(timedelta(hours=8))
                        date = dt.astimezone(tzutc_8).strftime("%Y-%m-%d %H:%M:%S")

                    if IOT.is_used and user.is_used and user.rfid == IOT.rfid:
                        msg = """<h1>{} 您好:</h1>
                            <p style="color:red">您的愛車可能於{}時發生了問題</p>
                            <p>請盡快前去{}查看</p>
                            <br></br>
                            <br></br>
                            <br></br>
                            <span style="float:right">smart park關心您</span>
                            """.format(user.name, date, IOT.address)
                        message['error_request'] = False
                        mail.send(user.email, "Smart park 緊急通知", msg)

                    user.save()
                    IOT.save()

                await client.publish(str(topic), bytes(json.dumps(message),'utf-8'))

            except (json.decoder.JSONDecodeError, db.IOT.DoesNotExist, db.User.DoesNotExist) as err:
                await client.publish(str(topic), bytes(json.dumps(message),'utf-8'))
                logger.error("Client subscribe exception: {}".format(err))
            
    except ClientException as ce:
        logger.error("Client exception: {}".format(ce))


def start_sub(loop=asyncio.new_event_loop()):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(uptime_coro())
    loop.run_forever()


if __name__ == "__main__":
    start_sub()
