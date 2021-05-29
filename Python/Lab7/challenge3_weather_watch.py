from pyowm import OWM
import datetime
import time

# ser= serial.Serial(port ='/dec/cu.SLAB_USBtoUART',baudrate = 115200)
#/dev/cu.Maria-ESP32SPP
#/dev/cu.SLAB_USBtoUART'

# each line 17 chars
def getWeather():
    # Retrieves the weather in Fahrenheit
    weather = owm.weather_at_place('Los Angeles, CA, US').weather
    temperature = weather.temperature('fahrenheit')
    # Output = dictionary
    # {'temp': 55.76, 'temp_max': 57.99, 'temp_min': 52.0, 'feels_like': 54.43, 'temp_kf': None}

    line1 = 'Temp: %sF' % (temperature['temp'])
    line2 = 'Feels like %sF' % (temperature['feels_like'])
    line3 = 'H&L: %s/%s' % (temperature['temp_max'], temperature['temp_min'])
    # return line1 + ',' + line2 + ',' + line3
    return line1


def getTime():
    # Retrieve the local time and date
    data = time.localtime()
    # Output = struct (read-only)
    # time.struct_time(tm_year=2021, tm_mon=4, tm_mday=25, tm_hour=21, tm_min=31, tm_sec=51, tm_wday=6, tm_yday=115, tm_isdst=1)

    currentdate = f'{data.tm_mon}/' + f'{data.tm_mday}/' + f'{data.tm_year % 100}'

    # Formatting minutes to 00,01,02,...,09 since struct formatted as as 0,1,2,...,9
    if data.tm_min < 10:
        if data.tm_min == 0:
            minutes = '00'
        minutes = '0' + f'{data.tm_min}'
    else:
        minutes = data.tm_min

    # Formats military time to 12-hour time
    if data.tm_hour > 12:
        hour = data.tm_hour - 12
        currenttime = f'{hour}:' + f'{minutes}' + 'pm'

    elif data.tm_hour == 12:
        currenttime = f'{data.tm_hour}:' + f'{minutes}' + 'pm'

    else:
        currenttime = f'{data.tm_hour}:' + f'{minutes}' + 'am'

    return currentdate + ' ' + currenttime


def getData():
    # Formats the final message to be sent to OLED
    return getTime() + ',' + getWeather()


# Starts by initializing the connection to OpenWeatherMap API
owm = OWM('e482c993580ee6a821590ea831c2de24').weather_manager()