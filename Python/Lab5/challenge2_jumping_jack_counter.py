from ECE16Lib.Communication import Communication
from ECE16Lib.Pedometer import JumpingJacksCounter

from matplotlib import pyplot as plt
from time import time, sleep

previousMessage = ""
previousax = 0
ax = 0

if __name__ == "__main__":
    fs = 50  # sampling rate
    num_samples = 512  # 10 seconds of data @ 50Hz
    process_time = 1

    # Initialize the counter
    jack = JumpingJacksCounter(num_samples, fs, [])

    comms = Communication("/dev/cu.MariaBT-ESP32SPP", 115200)
    comms.clear()  # just in case any junk is in the pipes

    comms.send_message("wearable")  # begin sending data
    sleep(0.5)
    # Initialize the counter on the MCU to display 0
    comms.send_message("0")

    try:
        previous_time = time()
        while (True):
            message = comms.receive_message()

            if (message != None):
                try:
                    (m1, m2, m3, m4) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
                    continue

                # Collect data in the pedometer
                jack.add(int(m2), int(m3), int(m4))
                ax = int(m2)


            # If there are no more messages, update the Counter
            else:
                current_time = time()
                if previousMessage == None and message == None:
                    if previousax != ax:
                        steps, peaks, filtered = jack.process()
                        print("Step count: {:d}".format(steps))

                        comms.send_message(f"{steps}")
                        plt.cla()
                        plt.plot(filtered)
                        plt.title("Jumping Jack Count: %d" % steps)
                        plt.show(block=False)
                        plt.pause(1)
                        previousax = ax
            previousMessage = message

    except(Exception, KeyboardInterrupt) as e:
        print(e)  # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()