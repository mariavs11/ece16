from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np

def averageof(ax):
    return np.average(np.array(ax))

def sample_difference(ax):
    np.diff(np.array(ax))
    return np.diff(np.array(ax))

def L2_norm(ax,ay,az):
    # turn inputs into an array
    #linalg will return the eucledian distance
    return np.linalg.norm(np.array([ax,ay,az]))

def L1_norm(ax,ay,az):
    #linalgn with ord=1 will return the max absolute value of the sum of ax,ay and az
    return np.linalg.norm(np.array([ax, ay, az]), ord=1)

def sineof(ax): # transformation 5
   return np.sin(np.array(ax)) # returns the sine of ax


if __name__ == "__main__":
  num_samples = 250    # 5 seconds of data @ 50Hz
  refresh_time = 0.1              # update the plot every 0.1s (10 FPS)
  # CREATE FOUR RAW DATA CIRCULAR LISTS
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  average_x = CircularList([], num_samples)
  delta_x = CircularList([], num_samples)
  L1= CircularList([], num_samples)
  L2 = CircularList([], num_samples)
  transformed = CircularList([], num_samples)

  comms = Communication("/dev/cu.SLAB_USBtoUART", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data
  transform = "sineof"  #set the type of transformation

  try:
    previous_time = 0
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue


        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))

        L1.add(L1_norm(ax,ay,az))
        L2.add(L2_norm(ax, ay, az))
        delta_x = sample_difference(ax)
        average_x.add(averageof(ax))
        transformed = sineof(ax)

        # if enough time has elapsed, clear the axis, and plot az
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time

          if (True):
              plt.cla()
              #plt.subplot(211)
              plt.title('red(ax) blue(ay) green(az)')
              plt.plot(ax, 'r', ay, 'b', az, 'g')
              plt.subplot(212)
              plt.title('Average of ax')
              plt.plot(average_x)
              plt.show(block=False)
              plt.pause(0.001)

          if (False):
            plt.cla()
            plt.subplot(211)
            plt.title('Sample difference of ax')
            plt.plot(delta_x)
            plt.show(block=False)
            plt.pause(0.001)
          if (False):
            plt.subplot(131)
            plt.title('L2 norm of all axes')
            plt.plot(L2)

            plt.subplot(132)
            plt.title('L1 norm of all axes')
            plt.plot(L1)

            plt.subplot(133)
            plt.title('Sine of ax')
            plt.plot(transformed)

            plt.show(block=False)
            plt.pause(0.001)

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()

