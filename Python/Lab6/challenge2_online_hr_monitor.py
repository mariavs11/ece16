from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from matplotlib import pyplot as plt
from time import time
import numpy as np
from numpy.core.numeric import NaN
peaks = 0
if __name__ == "__main__":
    fs = 50  # sampling rate
    num_samples = 250  # 5 seconds of data @ 50Hz
    refresh_time = 1  # plot every second

    hr_monitor = HRMonitor(250, 50)

    comms = Communication("/dev/cu.SLAB_USBtoUART", 115200)
    comms.clear()  # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data

    try:
        previous_time = time()
        while (True):
            message = comms.receive_message()
            if (message != None):
                try:
                    (m1, m2) = message.split(',') #m1 = time and m2 = ppg
                except ValueError:  # if corrupted data, skip the sample
                    continue


                # Adding the sample time and value into the HRMonitor class
                hr_monitor.add(int(m1)/1000, int(m2)) # changed time from milli to seconds

                # if enough time has elapsed, process the data and send the HR
                current_time = time()
                if (current_time - previous_time > refresh_time):
                    previous_time = current_time
                    # run hrmonitor class
                    hr_monitor.process()

                    if (peaks == 0):
                    # if no peaks were detected, don't send heart rate
                      print("no data")
                      hr, peaks = hr_monitor.process()
                      comms.send_message("NOT ENOUGH DATA")
                    else:

                        hr,peaks,filtered = hr_monitor.process()
                        comms.send_message("{:.2f}".format(hr))
                        plt.cla()
                        plt.plot(filtered)
                        plt.title("Estimated Heart Rate: {:.2f} bpm".format(hr))
                        plt.show(block=False)
                        plt.pause(0.0001)
    except(Exception, KeyboardInterrupt) as e:
        print(e)  # exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()