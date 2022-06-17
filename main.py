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
    # Print data
    tempC, presPa, humRH = sensor.values() # read all data from the sensor
    pres_hPa = presPa / 100 # convert air pressurr Pascals -> hPa (or mbar, if you prefer)
    print(str(tempC)+" °C  " + str(pres_hPa)+" hPa  " + str(humRH)+" %RH")
    
    # Altitude demo
    #print(sensor.altitude() - zeroAlt) # Print the pressure CHANGE since the script began

    # Read and print light data
    lightVal = light.read()
    print(str(lightVal) + " lux")
    
    sleep_ms(500)