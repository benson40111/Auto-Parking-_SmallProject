import time, asyncio
from datetime import datetime, timezone, timedelta
from app import logger


def observer(loop,sr04, motor_locked, client):
    logger.info('observer start')
    while True:
        if motor_locked.status and motor_locked.uid != "SYSTEM_LOCKED" and sr04.distance() > 50:
            date = datetime.now()
            errors = 0
            for x in range(6):
                if sr04.distance() > 50:
                    errors += 1
                time.sleep(10)

            if errors > 3:
                dt = datetime.utcnow().replace(tzinfo=timezone.utc)
                tzutc_8 = timezone(timedelta(hours=8))
                local_dt = dt.astimezone(tzutc_8).strftime("%Y-%m-%d %H:%M:%S")
                message = {
                        'method': 'ERROR',
                        'number': client.number,
                        'rfid': motor_locked.uid,
                        'time': local_dt
                        }
                if motor_locked.status:
                    loop.run_until_complete(client.publish(message))
        
        time.sleep(30)

