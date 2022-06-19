import time

from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030

# initalise the sensors
sensor = PiicoDev_BME280()
light = PiicoDev_VEML6030()

# take an initial altitude reading
zeroAlt = sensor.altitude()

for i in range(100):
    # read and assign the sesnor values
    tempC, presPa, humRH = sensor.values()
    lightLux = light.read()

    # convert air pressure Pascals -> hPa
    pres_hPa = presPa / 100

    # print the sensor values
    print(str(i), str("{:.2f}".format(tempC))+"°C", str("{:.2f}".format(pres_hPa))+"hPa ", str("{:.2f}".format(humRH))+"%RH ", str("{:.2f}".format(lightLux)) + "lux")

    time.sleep(5)