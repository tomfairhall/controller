# Controller v0.1.1
# CSV file order: date-time, temp, pressure, humidity, lux
# Cron Job running every 30 mins: */30 * * * * /usr/bin/python3 /home/admin/Documents/controller/main.py

import argparse
import csv
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

temp_C = []
pres_HPa = []
hum_RH = []
light_Lx = []

for x in range(3):
    # read and assign the sesnor values
    temp_C[x], (pres_HPa/100)[x], hum_RH[x] = bme280.values()
    light_Lx[x] = veml6030.read()

temp_C_ave = sum(temp_C)/len(temp_C)
pres_HPa_ave = sum(pres_HPa)/len(pres_HPa)
hum_RH_ave = sum(hum_RH)/len(hum_RH)
light_Lx_ave = sum(light_Lx)/len(light_Lx)

# output handiling
if(args.read):
    print(now, str(temp_C_ave), str(pres_HPa_ave), str(hum_RH_ave), str(light_Lx_ave))
elif(args.write):
    # open, or create a file in append mode and write the environmental varaibles to a cvs file
    with open('/home/admin/Documents/controller/data.csv', 'a', newline='') as file:      
        writer = csv.writer(file)
        writer.writerow([now, str(temp_C_ave), str(pres_HPa_ave), str(hum_RH_ave), str(light_Lx_ave)])