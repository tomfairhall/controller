# Controller
#* VERSION:
# v0.1.0
#* NOTES:
# CSV file order: date-time, temp, pressure, humidity, lux
# Cron Job running every 30 mins: */30 * * * * /usr/bin/python3 /home/admin/Documents/controller/main.py

import argparse
import csv
from statistics import mean
from datetime import datetime
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030

# initialize the input argument parser
parser = argparse.ArgumentParser()

# add arguments
parser.add_argument("-r", "--read", help="read measurements to terminal", action="store_true")
parser.add_argument("-w", "--write", help="write measurements to file", action="store_true")

# parse input arguments
args = parser.parse_args()

# get the current date and time
now = datetime.now()

def measure_data(sample_size):

    # initialise the sensors
    bme280 = PiicoDev_BME280()
    veml6030 = PiicoDev_VEML6030()

    # read and assign initial altitude reading
    zero_alt = bme280.altitude()

    # initialise sensor value lists
    temp_C_values = []
    pres_HPa_values = []
    hum_RH_values = []
    light_Lx_values = []

    for x in range(sample_size):
        # read and assign the sensor values !! rem to div by 100
        temp_C, pres_Pa, hum_RH = bme280.values()
        light_Lx = veml6030.read()

        temp_C_values.append(temp_C)
        pres_HPa_values.append(pres_Pa/100)
        hum_RH_values.append(hum_RH)
        light_Lx_values.append(light_Lx)
    
    # find average of measurement values
    temp_C_ave = round(mean(temp_C_values), 2)
    pres_HPa_ave = round(mean(pres_HPa_values), 2)
    hum_RH_ave = round(mean(hum_RH_values), 2)
    light_Lx_ave = round(mean(light_Lx_values), 2)

    return temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave    

temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave = measure_data(3)

# output handling
if(args.read):
    print("Time-date:", now)
    print("Temperature:", str(temp_C_ave) + "°C")
    print("Pressure:", str(pres_HPa_ave) + "HPa")
    print("Humidity:", str(hum_RH_ave) + "RH")
    print("Lux:", str(light_Lx_ave) + "Lux")
elif(args.write):
    # open, or create a file in append mode and write the environmental variables to a cvs file
    with open('/home/pi/Documents/controller/data.csv', 'a', newline='') as file:      
        writer = csv.writer(file)
        writer.writerow([now, str(temp_C_ave), str(pres_HPa_ave), str(hum_RH_ave), str(light_Lx_ave)])