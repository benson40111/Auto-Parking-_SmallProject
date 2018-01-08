import time
 
class motor:
    def __init__(self, GPIO):
        self.GPIO = GPIO
        self.forward_sq = ['0011', '1001', '1100', '0110']
        self.reverse_sq = ['0110', '1100', '1001', '0011']
        self.pin = [31, 33, 35, 37]
        for i in range(4):
            GPIO.setup(self.pin[i], GPIO.OUT)

    def set_motor(self, step):
        for i in range(4):
            self.GPIO.output(self.pin[i], step[i] == '1')

    def forward(self, steps, delay):
        for i in range(steps):
            for step in self.forward_sq:
                self.set_motor(step)
                time.sleep(delay)

    def reverse(self, steps, delay):
        for i in range(steps):
            for step in self.reverse_sq:
                self.set_motor(step)
                time.sleep(delay)

    def reset_motor(self):
        self.set_motor('0000')
