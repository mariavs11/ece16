from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from matplotlib import pyplot as plt
from time import time
import numpy as np
from numpy.core.numeric import NaN

if __name__ == "__main__":
    fs = 50  # sampling rate
    num_samples = 500  # 10 seconds of data @ 50Hz
    refresh_time = 1  # plot every second

    # Establish Communication with MCU
    comms = Communication('/dev/cu.MariaBT-ESP32SPP', 115200)

    # Initialize and train HRMonitor class
    hr_monitor = HRMonitor(500, 50)
    hr_monitor.train()
    print("finished training")
    comms.clear()  # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data
    print("sent to wearable")
    try:
        previous_time = time()
        while (True):
            message = comms.receive_message()
            if (message != None):
                try:
                    (m1, m2) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
                    continue

                # Changing the time from milliseconds into seconds


                # Adding the sample time and value into the HRMonitor class
                hr_monitor.add((int(m1) / 1000), int(m2))  # changed time from milli to seconds
                # if enough time has elapsed, process the data and send the HR
                current_time = time()
                if (current_time - previous_time > refresh_time):
                    previous_time = current_time

                    # Predict heartrate from PPG data
                    heartrate = hr_monitor.predict()
                    comms.send_message("{:.2f}".format(heartrate))
                    if heartrate != np.NaN or heartrate == 0:
                        comms.send_message("{:.2f}".format(heartrate))
                    else :
                        comms.send_message("NOT ENOUGH DATA")

    except(Exception, KeyboardInterrupt) as e:
        print(e)  # exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()



