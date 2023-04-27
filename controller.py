import argparse
import sqlite3
from statistics import mean
from datetime import datetime
from PiicoDev_RGB import PiicoDev_RGB
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030
from PiicoDev_TMP117 import PiicoDev_TMP117

DATABASE_PATH = '/home/controller/data.db'
DATABASE_SCHEMA_PATH = '/home/controller/controller/schema.sql'
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
READ_LED = 0
WRITE_LED = 1

# Initialize the input argument parser, add and parse input arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--write", help="write measurements to file", action="store_true")
parser.add_argument("-r", "--read", help="read measurements to terminal", action="store_true")
args = parser.parse_args()

# Initalize the LED display.
light = PiicoDev_RGB()

def light_on():
    light.fill([255, 255, 255])

def light_off():
    light.clear()

def light_reading():
    light.setPixel(READ_LED, GREEN)
    light.show()

def light_writing():
    light.setPixel(WRITE_LED, GREEN)
    light.show()

def measure_time():
    # Get the current date and time.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def measure_temp(sensor: PiicoDev_TMP117):
    light_reading()
    measurement = sensor.readTempC()
    light_off()
    return measurement

def measure_pres(sensor: PiicoDev_BME280):
    light_reading()
    _, measurement, _ = sensor.values()
    light_off()
    return measurement

def measure_hum(sensor: PiicoDev_BME280):
    light_reading()
    _, _, measurement = sensor.values()
    light_off()
    return measurement

def measure_light(sensor: PiicoDev_VEML6030):
    light_reading()
    measurement = sensor.read()
    light_off()
    return measurement

# Measure data and average 3 times to limit any outliers in measurement.
def measure_data(sample_size=3):
    # Initialise the sensors.
    bme280 = PiicoDev_BME280()
    veml6030 = PiicoDev_VEML6030()
    tmp117 = PiicoDev_TMP117()

    # Read and assign initial altitude reading.
    zero_alt = bme280.altitude()

    # Initialise sensor value lists.
    temp_C_values = []
    pres_HPa_values = []
    hum_RH_values = []
    light_Lx_values = []

    date_time = measure_time()

    for x in range(sample_size):
        # Read and assign the sensor values.
        temp_C = measure_temp(tmp117)
        pres_Pa = measure_pres(bme280)
        hum_RH = measure_hum(bme280)
        light_Lx = measure_light(veml6030)

        temp_C_values.append(temp_C)
        pres_HPa_values.append(pres_Pa/100)
        hum_RH_values.append(hum_RH)
        light_Lx_values.append(light_Lx)

    # Find average of measurement values.
    temp_C_ave = round(mean(temp_C_values), 2)
    pres_HPa_ave = round(mean(pres_HPa_values), 2)
    hum_RH_ave = round(mean(hum_RH_values), 2)
    light_Lx_ave = round(mean(light_Lx_values), 2)

    return date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave

def write_data(data: tuple):
    light_writing()

    conn = sqlite3.connect(DATABASE_PATH)
    with open(DATABASE_SCHEMA_PATH, mode='r') as schema:
        conn.cursor().execute(schema.read())
    conn.execute('INSERT INTO measurements VALUES(?, ?, ?, ?, ?)', (data[0], data[1], data[2], data[3], data[4]))
    conn.commit()
    conn.close()

    light_off()

# Controller logic handeler.
def controller():
    if (args.read or args.write):
        data = measure_data()
        if (args.write):
            write_data(data)
        elif (args.read):
            print("Date-Time:\t", data[0])
            print("Temperature:\t", str(data[1]) + "°C")
            print("Pressure:\t", str(data[2]) + "HPa")
            print("Humidity:\t", str(data[3]) + "RH")
            print("Light:\t\t", str(data[4]) + "lx")

controller()