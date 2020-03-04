from machine import Pin, I2C, PWM
import onewire, ds18x20
from time import sleep
from lcd_lib.esp8266_i2c_lcd import I2cLcd, DEFAULT_I2C_ADDR
from time import sleep_ms, ticks_ms
import math
import utime
import random
import dht

i2c = I2C(scl=Pin(32), sda=Pin(33), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
ds_pin = Pin(15)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))


led = Pin(2, Pin.OUT)

PIN_R = 27
PIN_G = 26
PIN_B = 25

class RGBLed:
    def __init__(self, pin_r, pin_g, pin_b):
        self.pin_r = PWM(Pin(pin_r))
        self.pin_g = PWM(Pin(pin_g))
        self.pin_b = PWM(Pin(pin_b))
        self.set(0, 0, 0)

    def set(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.duty()

    def duty(self):
        self.pin_r.duty(self.duty_translate(self.r))
        self.pin_g.duty(self.duty_translate(self.g))
        self.pin_b.duty(self.duty_translate(self.b))

    def duty_translate(self, n):
        """translate values from 0-255 to 0-1023"""
        return int((float(n) / 255) * 1023)

rgb_leb = RGBLed(PIN_R, PIN_G, PIN_B)

dht22 = dht.DHT22(Pin(15))


lcd.backlight_on()
current_temp = 0.0
current_r = 0.0
current_g = 0.0
current_b = 0.0

humidity = 0.0
start = utime.ticks_ms()
count = 0

def calc_by_time(counter, delta=0):
    return math.sin(((counter * 20 + delta) % 360) * math.pi / 180) / 2 + 0.5


while True:
    try:
        sleep(1)
        count += 1
        time_delta = utime.ticks_diff(utime.ticks_ms(), start)
        if time_delta > 3000:
            dht22.measure()
            current_temp = dht22.temperature()
            humidity = dht22.humidity()
            start = utime.ticks_ms()


        current_r = calc_by_time(count)
        current_g = calc_by_time(count, 120)
        current_b = calc_by_time(count, 240)
        print("%s %s %s" %(current_r, current_g, current_b))

    except Exception as identifier:
        pass
    finally:
        lcd.move_to(0, 0)
        lcd.putstr("T:%2.1f H:%2.1f\nMerry XMAS (^_^)" % (current_temp, humidity))
        rgb_leb.set(int(255 * current_r), int(255 * current_g), int(255 * current_b))


