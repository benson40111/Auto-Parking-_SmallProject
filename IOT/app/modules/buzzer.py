import time

class buzzer:
    def __init__(self, GPIO, Feq=2600):
        self.GPIO = GPIO
        self.pin = 29
        self.Feq = 2600
        self.GPIO.setup(self.pin, GPIO.OUT)

    def ring(self, t=0.1):
        buzzer = self.GPIO.PWM(self.pin, self.Feq)
        buzzer.start(50)
        time.sleep(t)
        buzzer.stop()

    def warning(self, t=0.1):
        for x in range(2):
            buzzer = self.GPIO.PWM(self.pin, self.Feq)
            buzzer.start(50)
            time.sleep(t)
            buzzer.stop()
            time.sleep(t)
