from app import logger, GPIO
from app.modules.mqtt import mqtt
from app.modules import buzzer as Buzzer
from hbmqtt.client import ClientException
import threading, asyncio
import json


buzzer = Buzzer.buzzer(GPIO)

async def uptime_coro(lock, motor, motor_locked):
    client =mqtt()
    logger.info("mqtt client ready")
    await client.subscribe()
    while True:
        try:
            message = await client.wait_for_message()
            NAV = message.get('error_request', None) # Not a vaild
            if not NAV:
                method = message.get('method', None)
                locked = message.get('locked', None)
                uid = message.get('rfid', None)
                if method == 'GET':
                    is_used = message.get('is_used', None)
                    if is_used != None:
                        motor_locked.uid = uid
                        motor_locked.status = is_used
                elif method == 'POST' or method == 'SYSTEM':
                    buzzer.ring()
                    if locked:
                        if method == 'POST':
                            lock.acquire()
                        motor.reset_motor()
                        motor.forward(720, 0.002)
                        motor.reset_motor()
                        motor_locked.uid = uid
                        motor_locked.status = locked
                        if method == 'POST':
                            lock.release()
                    if locked == False:
                        if method == 'POST':
                            lock.acquire()
                        motor.reset_motor()
                        motor.reverse(720, 0.002)
                        motor.reset_motor()
                        motor_locked.uid = uid
                        motor_locked.status = locked
                        if method == 'POST':
                            lock.release()
            else:
                buzzer.warning()


        except Exception as err:
            lock.release()
            logger.error("Client subscribe: {}".format(err))


def start_sub(loop, lock, motor, motor_locked):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(uptime_coro(lock, motor, motor_locked))
    loop.run_forever()
