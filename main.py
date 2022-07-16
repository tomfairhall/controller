from datetime import datetime
import csv

from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030

print("Starting...")

# initalise the sensors
bme280 = PiicoDev_BME280()
veml6030 = PiicoDev_VEML6030()

# take an initial altitude reading
zeroAlt = bme280.altitude()

# read and assign the sesnor values
tempC, presPa, humRH = bme280.values()
lightLx = veml6030.read()

# convert air pressure Pascals -> hPa
presHPa = presPa / 100

now = datetime.now()

with open('data.csv', 'a', newline='') as file:
    writer = csv.writer(file)     
    writer.writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), str(tempC), str(presHPa), str(humRH), str(lightLx)])

print("Complete")