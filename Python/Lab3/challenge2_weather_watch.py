import serial
import time   # for timing purposes
from pyowm import OWM
from datetime import datetime

owm = OWM('e482c993580ee6a821590ea831c2de24').weather_manager()
today = datetime.today() # use this library to find out the date

# ser= serial.Serial(port ='/dec/cu.SLAB_USBtoUART',baudrate = 115200)
#/dev/cu.Maria-ESP32SPP
#/dev/cu.SLAB_USBtoUART'
def setup(serial_name, baud_rate):
    ser = serial.Serial(serial_name, baudrate = baud_rate)
    return ser

def close(ser):
    ser.close()

def send_message(ser, message):
   if(message[-1] != '\n'):

       message = message + '\n'
   ser.write(message.encode('utf-8'))



def receive_message(ser, num_bytes=50):
    if(ser.in_waiting > 0):
        return ser.readline(num_bytes).decode('utf-8')
    else:
        return None

def main():
    time.sleep(3)
    ser = setup('/dev/cu.MariaBT-ESP32SPP', 115200)
    time.sleep(3)
    while (True):
       weather = owm.weather_at_place('San Diego,CA,US').weather # contains info about the weather
       x = weather.detailed_status # contains description about weather
       temp = weather.temperature('celsius') # this returns a dictionary
       temp = temp['temp'] # accesses value in dictionary temp
       temp = str(temp)+ " Celsius " # converts temp into a string and adds "Celsius"
       now = datetime.now()
       current_time = now.strftime("%H:%M:%S") # stores current time
       d = today.strftime("%m/%d/%y") # stores date
       send_message(ser, temp + "," + current_time + ","+ d +"," + x)

    close(ser)

"""
Main entrypoint for the application
"""
if __name__== "__main__":
    main()
