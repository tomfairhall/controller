import argparse
import sqlite3
from statistics import mean
from datetime import datetime
from PiicoDev_RGB import PiicoDev_RGB
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030
from PiicoDev_TMP117 import PiicoDev_TMP117
from subprocess import run

DATABASE_PATH = '/home/controller/data.db'
DATABASE_SCHEMA_PATH = '/home/controller/controller/schema.sql'

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
READ_LED = 0
WRITE_LED = 1

class Display(object):
    def __init__(self, light_output: PiicoDev_RGB, mode):
        self._light_ouput = light_output
        self._mode = mode

    def __enter__(self):
        if self._mode == 'r' or self._mode == 'read':
            self.__set_light_on(led_index=READ_LED, colour=GREEN)
        elif self._mode == 'w' or self._mode == 'write':
            self.__set_light_on(led_index=WRITE_LED, colour=GREEN)

    def __exit__(self, exc_type, exc_val, traceback):
        self.__light_off()

    def __set_light_on(self, led_index, colour):
        self._light_ouput.setPixel(led_index, colour)
        self._light_ouput.show()

    def __light_off(self):
        self._light_ouput.clear()

# Initialize the input argument parser, add and parse input arguments.
parser = argparse.ArgumentParser(description="System Controller")
parser.add_argument('-r', '--read', help="read measurements to terminal", action='store_true')
parser.add_argument('-w', '--write', help="write measurements to file", action='store_true')
parser.add_argument('repeat', nargs='?', help="number of times to read/write", default=1, type=int)
args = parser.parse_args()

# Initalize the LED display.
light = PiicoDev_RGB()

def get_time():
    with Display(light, mode='read'):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def get_temperature(sensor: PiicoDev_TMP117):
    with Display(light, mode='read'):
        return sensor.readTempC()

def get_pressure(sensor: PiicoDev_BME280):
    with Display(light, mode='read'):
        _, measurement, _ = sensor.values()
        return measurement

def get_humidity(sensor: PiicoDev_BME280):
    with Display(light, mode='read'):
        _, _, measurement = sensor.values()
        return measurement

def get_light(sensor: PiicoDev_VEML6030):
    with Display(light, mode='read'):
        return sensor.read()

# Measure data and average 3 times to limit any outliers in measurement.
def read_data(sample_size=3):
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

    date_time = get_time()

    for _ in range(sample_size):
        # Read and assign the sensor values.
        temp_C_values.append(get_temperature(tmp117))
        pres_HPa_values.append((get_pressure(bme280))/100)
        hum_RH_values.append(get_humidity(bme280))
        light_Lx_values.append(get_light(veml6030))

    # Find average of measurement values.
    temp_C_ave = round(mean(temp_C_values), 2)
    pres_HPa_ave = round(mean(pres_HPa_values), 2)
    hum_RH_ave = round(mean(hum_RH_values), 2)
    light_Lx_ave = round(mean(light_Lx_values), 2)

    return date_time, temp_C_ave, pres_HPa_ave, hum_RH_ave, light_Lx_ave

def write_data(data: tuple):
        with Display(light, mode='write'):
            connection = sqlite3.connect(DATABASE_PATH)
            with open(DATABASE_SCHEMA_PATH, mode='r') as schema:
                connection.execute(schema.read())
            connection.execute('INSERT INTO measurements VALUES(?, ?, ?, ?, ?)', (data[0], data[1], data[2], data[3], data[4]))
            connection.commit()
            connection.close()

if __name__ == '__main__':
    for _ in range(args.repeat):
        data = read_data()
        if args.write:
            write_data(data)
        if args.read:
            print("Date-Time:\t", data[0])
            print("Temperature:\t", str(data[1]) + "°C")
            print("Pressure:\t", str(data[2]) + "HPa")
            print("Humidity:\t", str(data[3]) + "RH")
            print("Light:\t\t", str(data[4]) + "lx")