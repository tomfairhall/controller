# PiicoDev Atmospheric Sensor BME280 minimal example code
# This program reads Temperature, Pressure and Relative Humididty
# from the PiicoDev Atmospheric Sensor. An altitude reading is also
# available

from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030
from PiicoDev_Unified import sleep_ms # cross-platform compatible sleep function

sensor = PiicoDev_BME280() # initialise the sensor
light = PiicoDev_VEML6030()

zeroAlt = sensor.altitude() # take an initial altitude reading

while True:
    tempC, presPa, humRH = sensor.values() # read all data from the sensor
    pres_hPa = presPa / 100 # convert air pressurr Pascals -> hPa (or mbar, if you prefer)

    lightVal = light.read()

    print('%.2f' % str(tempC)+" °C " + '%.2f' % str(pres_hPa)+" hPa " + '%.2f' % str(humRH)+" %RH " + '%.2f' % str(lightVal) + " lux")

    sleep_ms(100)