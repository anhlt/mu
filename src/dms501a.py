import machine
from machine import Pin, time_pulse_us
import utime

class DMS501(object):

    def __init__(self, pin10, pin25):
        super().__init__()
        self.pin10 = pin10
        self.pin25 = pin25
        self.sample_time_ms = 3000

    @property
    def pm25(self):
        total_low_duration = 0.0

        start_time = utime.ticks_ms()
        while True:
            end_time = utime.ticks_ms()
            if (end_time - start_time) > self.sample_time_ms:
                break
            low_time = time_pulse_us(self.pin25, 0) / 1000.0
            print(low_time)
            print("endtime %f" % (end_time - start_time))
            print("total_low_duration %f" % total_low_duration)

            total_low_duration += low_time

        print("\n")
        print(total_low_duration)
        print(end_time - start_time)
        ratio = (total_low_duration) / (end_time -  start_time) * 100
        print("Ratio %f" % ratio)
        return ratio
