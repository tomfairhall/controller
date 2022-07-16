import datetime

from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_VEML6030 import PiicoDev_VEML6030

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

try:
    f = open("data.txt", "a")

    f.write(datetime.datetime.now())
    f.write(tempC)
    f.write(presHPa)
    f.write(humRH)
    f.write(lightLx)

except FileNotFoundError:
    print("File not accessible")
    
finally:
    f.close()


# print the sensor values
# print(str(i), str("{:.2f}".format(tempC))+"°C", str("{:.2f}".format(presHPa))+"hPa ", str("{:.2f}".format(humRH))+"%RH ", str("{:.2f}".format(lightLx)) + "lux")