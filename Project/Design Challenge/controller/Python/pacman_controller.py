"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.DSP import moving_average
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
from time import sleep,time
import socket, pygame
import numpy as np

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)


class PygameController:
  comms = None

  def __init__(self, serial_name, baud_rate):
    self.comms = Communication(serial_name, baud_rate)
    self.x = CircularList([],20)
    self.y = CircularList([],20)
    self.z = CircularList([],20)

  def getOrientation(self):
    # Computes the moving average of the three accelerometer values
    x_avg = filt.moving_average(np.array(self.x),5)
    y_avg = filt.moving_average(np.array(self.y),5)
    z_avg = filt.moving_average(np.array(self.z),5)

    # Use only the most recent moving average value
    x = x_avg[-1]
    y = y_avg[-1]
    z = z_avg[-1]

    # Use thresholding to determine orientation
    # For Horizontal Movements
    if abs(x) >= 100:
        if x < 0:
            command_hori = "LEFT"
        else:
            command_hori = "RIGHT"
    else:
      command_hori = None

    # For Vertical Movements
    if abs(y) >= 100:
        if y < 0:
            command_vert = "DOWN"
        else:
            command_vert = "UP"
    else:
        command_vert = None

    return command_hori, command_vert

  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    self.comms.send_message("stop")
    self.comms.clear()

    # 2a. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # 2b. Sending to give game the address
    mySocket.send("CONTROLLER".encode("UTF-8"))

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")

    data = None
    score = None
    lives = None

    prevCommand = None
    
    sleep(1)

    previousTime = time()
    while True:
      message = self.comms.receive_message()

      # Check if server sends any commands (BUZZ)
      try: 
        data = mySocket.recv(1024).decode("utf-8")
      except BlockingIOError:
        pass

      # Tells MCU to vibrate when hit by a ghost
      if data == "BUZZ":
        self.comms.send_message("BUZZ")
        data = None

      # Decides whether to update lives/score on OLED display
      elif data != None:
        # Splits data into the text and number
        text, num = data.split(":")

        # If the score has changed, update OLED
        if text == "Score" and score != int(num):
          print(data)
          score = int(num)
          self.comms.send_message(data)

        # If the number of lives changed, update OLED
        elif text == "Lives" and lives != int(num):
          print(data)
          lives = int(num)
          self.comms.send_message(data)
    
      # While the game is running, determine orientation and send command to server
      if(message != None):
        command_hori = None
        command_vert = None

        [m1, m2, m3] = message.split(',')
        # Format: x, y, z
        # Accelerometer values are zeroed 

        # Add to Circularlist
        self.x.add(int(m1))
        self.y.add(int(m2))
        self.z.add(int(m3))

        # After certain time, get controller orientation and send command to server
        currentTime = time()
        if (currentTime - previousTime >= 0.01):
          previousTime = currentTime
          command_hori, command_vert = self.getOrientation()

          # If the commands are not None, send the input to the server
          # Sends the command only if the direction has changed
          if command_hori is not None and command_hori != prevCommand:
            mySocket.send(command_hori.encode("UTF-8"))
            prevCommand = command_hori
          elif command_vert is not None and command_vert != prevCommand:
            mySocket.send(command_vert.encode("UTF-8"))
            prevCommand = command_vert



if __name__== "__main__":
  serial_name = "COM5"
  baud_rate = 115200
  controller = PygameController(serial_name, baud_rate)

  try:
    controller.run()
  except(Exception, KeyboardInterrupt) as e:
    print(e)
  finally:
    print("Exiting the program.")
    controller.comms.send_message("stop")
    controller.comms.close()
    mySocket.send("QUIT".encode("UTF-8"))
    mySocket.close()

  input("[Press ENTER to finish.]")
