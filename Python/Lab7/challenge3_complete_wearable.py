from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.Pedometer import Pedometer
from time import time
import numpy as np
from numpy.core.numeric import NaN

# Import OWM library and functions from challenge3_weather_watch.py
import challenge3_weather_watch as watch

if __name__ == "__main__":
    fs = 50  # sampling rate
    num_samples = 500  # 10 seconds of data @ 50Hz
    refresh_time = 1  # plot every second

    # Establish Communication with MCU
    comms = Communication('/dev/cu.MariaBT-ESP32SPP', 115200)
    # Initialize and train HRMonitor GMM class
    hr_monitor = HRMonitor(num_samples, fs)
    hr_monitor.train()

    # Initialize Pedometer class
    ped = Pedometer(num_samples, fs, [])
    steps = 0

    comms.clear()  # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data

    try:
        previous_time = time()
        while (True):
            message = comms.receive_message()
            if message == "Step Counter":
                print(message)
            if (message != None):
                try:
                    (m1, m2, m3, m4, m5) = message.split(',')
                    # sampleTime, ax, ay, az, ppg
                except ValueError:  # if corrupted data, skip the sample
                    continue

                # Changing the time from milliseconds into seconds
                m1 = int(float(m1) / 1000)

                # Adding the sample time and the ppg value into the HRMonitor class
                hr_monitor.add(int(m1), int(m5))

                # If MCU is sending accelerometer data, add new sample
                # If data is 0, means Pedometer is off and don't update
                if int(m2) != 0:
                    # Adding the new accelerometer values into the Pedometer class
                    ped.add(int(m2), int(m3), int(m4))

                # if enough time has elapsed, process the data and send the HR and Step Count
                current_time = time()
                if (current_time - previous_time > refresh_time):
                    previous_time = current_time

                    # Process new PPG data
                    heartrate = hr_monitor.predict()

                    # Initiliaze the outgoing message to MCU
                    message1 = " HR: {:.2f} bpm  ".format(heartrate)

                    # Gets current time and temperature and appends to message
                    # Form : HR, time, temperature
                    message1 += "," + watch.getData()

                    # Only processes steps when the computer is receiving accelerometer data
                    # Accelerometer values of 0 mean that pedometer is off
                    if int(m2) != 0:
                        # Process new accelerometer data
                        try:
                            steps, ___, ___ = ped.process()
                        except Exception:
                            continue

                    # Appends the step count at the end
                    message1 += ", Step Count: {:d}".format(steps)

                    # Send message at the end
                    comms.send_message(message1)


    except(Exception, KeyboardInterrupt) as e:
        print(e)  # exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()