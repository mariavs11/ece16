from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
# from matplotlib import pyplot as plt
from time import time, time_ns
import numpy as np
from numpy.core.numeric import NaN
import cv2
import os

os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = 'T'
cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    fs = 50  # sampling rate
    num_samples = 500  # 10 seconds of data @ 50Hz
    refresh_time = 1  # plot every second

    hr_monitor = HRMonitor(500, 50)

    comms = Communication("/dev/cu.SLAB_USBtoUART", 115200)
    comms.clear()  # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data

    try:
        previous_time = time()
        while (True):
            _, frame = cap.read()

            new_sample = frame.mean(axis=0).mean(axis=0)
            new_sample = new_sample[2]   # uses the RED channel

            cv2.imshow('Input', frame)
            c = cv2.waitKey(1)
            if c == 27:
                break

            hr_monitor.add(int(new_sample), int(time_ns() / 1e9))

            # if enough time has elapsed, clear the axes, and plot the 4 plots
            current_time = time()
            if (current_time - previous_time > refresh_time):
                previous_time = current_time

                heartrate, peaks, ___ = hr_monitor.process()
                HR = "{:.2f}".format(heartrate)
                if HR == "nan":
                    comms.send_message("Not Enough Data")
                else:
                    comms.send_message(HR)


    except(Exception, KeyboardInterrupt) as e:
        print(e)  # exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
        cap.release()