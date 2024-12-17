from machine import Pin
from time import sleep_ms
x=Pin(13,Pin.OUT)
while True:
    x.on()
    sleep_ms(200)
    x.off()
    sleep_ms(200)