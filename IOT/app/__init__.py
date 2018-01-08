import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)
FORMAT = '[%(asctime)s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

