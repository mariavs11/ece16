import serial
import time   # for timing purposes
from challenge1_piglatin import *
#ser= serial.Serial(port ='/dec/cu.SLAB_USBtoUART',baudrate = 115200)
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
    ser = setup('/dev/cu.SLAB_USBtoUART', 115200)
    time.sleep(3)
    words = ["Quotient", "Mustn't", "Yellow","bye","apple"]
    output1 = english_to_pig_latin(words[3])
    print(output1)
    output2 = pig_latin_to_english(output1)
    print(output2)
    send_message(ser, output1 +  "," +output2)


    time.sleep(3)
    close(ser)

"""
Main entrypoint for the application
"""
if __name__== "__main__":
    main()
