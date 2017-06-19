from .common import DHT11, DHT22, AM2302, read, read_retry
from . import Raspberry_Pi_3_Driver as driver
import datetime
import time
import RPi.GPIO as GPIO
from DbClass import DbClass

def read(sensor, pin):
    # Validate pin is a valid GPIO.
    if pin is None or int(pin) < 0 or int(pin) > 31:
        raise ValueError('Pin must be a valid GPIO number 0 to 31.')
    # Get a reading from C driver code.
    result, humidity, temp = driver.read(sensor, int(pin))
    if result in common.TRANSIENT_ERRORS:
        # Signal no result could be obtained, but the caller can retry.
        return (None, None)
    elif result == common.DHT_ERROR_GPIO:
        raise RuntimeError('Error accessing GPIO.')
    elif result != common.DHT_SUCCESS:
        # Some kind of error occured.
        raise RuntimeError('Error calling DHT test driver read: {0}'.format(result))
    return (humidity, temp)


db = DbClass()

try:
    while True:
        tijdstip = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.setHumidityToDatabase(read(DHT22,4)[0], tijdstip)
        time.sleep(10)

except KeyboardInterrupt:
    pass

GPIO.cleanup()