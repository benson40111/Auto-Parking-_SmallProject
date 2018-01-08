from pirc522 import RFID
from app import GPIO, logger
from app.modules import sr04 as Sr04, motor as Motor, mqtt as Mqtt, buzzer as Buzzer
from app.conf import config
import time
from subscribe import start_sub
from observer import observer
from threading import Thread, Lock
import asyncio

debug = config.debug

if debug:
    logger.warning("Debug mode on")

rdr = RFID()
logger.info("rfid module ready")

sr04 = Sr04.sr04(GPIO)
logger.info("sr04 module ready")

motor = Motor.motor(GPIO)
motor.reset_motor()
logger.info("motor module ready")

client = Mqtt.mqtt(client_id="pub_"+str(config.number))
logger.info("mqtt client module ready")

buzzer = Buzzer.buzzer(GPIO)
logger.info("buzzer module ready")

class Motor_locked:
    def __init__(self):
        self.status = True
        self.uid = "SYSTEM_LOCKED"


if __name__ == '__main__':
    lock = Lock()
    motor_locked = Motor_locked()
    Thread(target=start_sub, args=(
        asyncio.new_event_loop(),
        lock,
        motor,
        motor_locked
        )).start()
    Thread(target=observer, args=(asyncio.get_event_loop(),sr04, motor_locked, client)).start()
    time.sleep(3)
    loop = asyncio.get_event_loop()
    message = {
            'method': 'GET',
            'number': client.number
            }
    loop.run_until_complete(client.publish(message))
    try:
        while True:
            time.sleep(1)
            try:
                lock.acquire()
                rdr.wait_for_tag()
                (error, data) = rdr.request()
                if not error:
                    logger.info("Detected")
                    (error, uid) = rdr.anticoll()
                    logger.info("uid: {}".format(str(uid)))
                    distance = sr04.distance(debug=debug)
                    if (distance < 50 and (not motor_locked.status)) or (motor_locked.status and motor_locked.uid == uid):
                        message = {
                                'method': 'POST',
                                'rfid': uid,
                                'number': client.number
                                }
                        loop.run_until_complete(client.publish(message))
                    else:
                        buzzer.warning()

                lock.release()

            except Exception as e:
                logger.error("RuntimeError: {}".format(e))
                lock.release()
    except:
        pass
