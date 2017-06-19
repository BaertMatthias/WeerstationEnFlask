from DbClass import DbClass
import RPi.GPIO as GPIO
import datetime

humidity, temperature = Adafruit_DHT.read_retry(2302, 4)

humidity = round(humidity, 2)
temperature = round(temperature, 2)

import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

def readChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8 | adc[2])
    return data

def berekenLichtsterkte():
    data_licht = readChannel(7)
    lichtsterkte = -(data_licht - 400)
    lichtsterkte = lichtsterkte / (400 - 10) * 100
    lichtsterkte = round(lichtsterkte,2)
    return lichtsterkte

db = DbClass()

try:
    while True:
        tijdstip = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.setLightToDatabase(berekenLichtsterkte(),tijdstip)
        time.sleep(10)
except KeyboardInterrupt:
    pass

GPIO.cleanup()

