# Controller v0.1.1
# CSV file order: date, time, temp, pressure, humidity, lux
# Cron Job running every 30 mins: */30 * * * * /usr/bin/python3 /home/admin/Documents/controller/main.py

import argparse
import csv
from datetime import datetime
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030

print("Starting...")

# initalise the input argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--read", help="read measurments", action="store_true")
parser.add_argument("-w", "--write", help="write measurments", action="store_true")
args = parser.parse_args()

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

# manual or automatic output of environmnetal varaibles
if(args.read):
    print(now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), str(temp_C), str(pres_HPa), str(hum_RH), str(light_Lx))
elif(args.write):
    # open, or create a file in append mode and write the environmental varaibles to a cvs file
    with open('/home/admin/Documents/controller/data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), str(temp_C), str(pres_HPa), str(hum_RH), str(light_Lx)])

print("Complete")