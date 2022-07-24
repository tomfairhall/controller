# Controller v0.1.1
# CSV file order: date-time, temp, pressure, humidity, lux
# Cron Job running every 30 mins: */30 * * * * /usr/bin/python3 /home/admin/Documents/controller/main.py

import argparse
import csv
from statistics import mean
from datetime import datetime
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030

# initalise the input argument parser
parser = argparse.ArgumentParser()

# add arguments
parser.add_argument("-r", "--read", help="read measurments", action="store_true")
parser.add_argument("-w", "--write", help="write measurments", action="store_true")

# parse input arguments
args = parser.parse_args()

# get the current date and time
now = datetime.now()

# initalise the sensors
bme280 = PiicoDev_BME280()
veml6030 = PiicoDev_VEML6030()

# read and assign initial altitude reading
zero_alt = bme280.altitude()

temp_C_values = []
pres_HPa_values = []
hum_RH_values = []
light_Lx_values = []

for x in range(3):
    # read and assign the sesnor values !! rem to div by 100
    temp_C, pres_HPa, hum_RH = bme280.values()
    light_Lx = veml6030.read()

    temp_C_values.append(temp_C)
    pres_HPa_values.append(pres_HPa/100)
    hum_RH_values.append(hum_RH)
    light_Lx_values.append(light_Lx)

temp_C_ave = mean(temp_C_values)
pres_HPa_ave = mean(pres_HPa_values)
hum_RH_ave = mean(hum_RH_values)
light_Lx_ave = mean(light_Lx_values)

# output handiling
if(args.read):
    print(now, str(temp_C_ave), str(pres_HPa_ave), str(hum_RH_ave), str(light_Lx_ave))
elif(args.write):
    # open, or create a file in append mode and write the environmental varaibles to a cvs file
    with open('/home/admin/Documents/controller/data.csv', 'a', newline='') as file:      
        writer = csv.writer(file)
        writer.writerow([now, str(temp_C_ave), str(pres_HPa_ave), str(hum_RH_ave), str(light_Lx_ave)])