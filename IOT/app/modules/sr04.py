import time
from app import logger


class sr04:
    def __init__(self, GPIO):
        self.GPIO = GPIO
        self.GPIO_TRIGGER = 3
        self.GPIO_ECHO = 5
        self.GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT )
        self.GPIO.setup(self.GPIO_ECHO, GPIO.IN)
        self.GPIO.output(self.GPIO_TRIGGER,False)
        time.sleep(0.5)

    def distance(self, debug = False):
        self.GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)
        self.GPIO.output(self.GPIO_TRIGGER, False)
        start = time.time()
        while self.GPIO.input(self.GPIO_ECHO) == 0:
            start = time.time()
        while self.GPIO.input(self.GPIO_ECHO) == 1:
            stop = time.time()
        elapsed= stop-start
        distance = elapsed * 34000 / 2.0
        if debug:
            logger.info("Distance: {0:.2f}".format(distance))
        return distance

