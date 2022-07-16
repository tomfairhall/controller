from datetime import datetime
import csv
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030

print("Starting...")

# initalise the sensors
bme280 = PiicoDev_BME280()
veml6030 = PiicoDev_VEML6030()

# take an initial altitude reading
zero_alt = bme280.altitude()

# read and assign the sesnor values
temp_C, pres_Pa, hum_RH = bme280.values()
light_Lx = veml6030.read()

# convert air pressure Pascals -> hPa
pres_HPa = pres_Pa / 100

# get the current date and time
now = datetime.now()

# open, or create a file in append mode and write the envrio varaibles
with open('/home/admin/Documents/data.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), str(temp_C), str(pres_HPa), str(hum_RH), str(light_Lx)])

print("Complete")