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
    if abs(x) >= 100:
      if x < 0:
        command = "LEFT"
      else:
        command = "RIGHT"
    else: # Controller is Flat
      command = None
    return command

  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    self.comms.send_message("stop")
    self.comms.clear()

    # 2a. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # 2b. Sending to server to share the address 
    mySocket.send("CONTROLLER".encode("UTF-8"))

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")

    # Initializing game state variables
    gameStart = False
    paused = False
    data = None

    # Wait for a second to allow enough readings to start computing moving average
    sleep(1) 

    previousTime = time()
    while True:
      message = self.comms.receive_message()

      # Check if server sends any commands (START,END,BUZZ)
      try: 
        data = mySocket.recv(1024).decode("utf-8")
      except BlockingIOError:
        pass

      # Tells MCU to vibrate when player is hit
      if data == "BUZZ":
        self.comms.send_message("BUZZ")
        data = None

      # Sends score to MCU to display on OLED if score has changed
      elif data != "END" and data != "START" and data != None:
        if score != int(data):
          score = int(data) # Updates local score to current
          self.comms.send_message(f"{score}")

      # When the game starts, start sending the commands from MCU to game
      if gameStart == False and data == "START":
        gameStart = True
        score = None
        self.comms.clear()
        data = None
      
      # Ran when player loses the game, stops Socket commands
      elif gameStart == True and data == "END":
        gameStart = False
        self.comms.clear()
        data = None
      
      # While the game is running, determine controller commands and send to game
      elif message != None and gameStart == True:
        command = None
        # message = int(message)

        [m1, m2, m3, m4, m5] = message.split(',')
        # Format: x, y, z, fire binary, pause binary
        # accelerometer values are zeroed 

        # Add to Circularlist
        self.x.add(int(m1))
        self.y.add(int(m2))
        self.z.add(int(m3))

        # Send FIRE command to sever if button was pressed
        if int(m4) == 1:
          mySocket.send("FIRE".encode("UTF-8"))

        # Tells game to toggle pause state if pause button was pressed
        # When game is paused, Socket commands aren't sent to server
        if int(m5) == 1:
          mySocket.send("PAUSE".encode("UTF-8"))
          print("Sent pause")
          if paused == True:
            paused = False
          else:
            paused = True

        # After certain time, filter the moving average and send Socket command
        currentTime = time()
        if (currentTime - previousTime >= 0.004):
          previousTime = currentTime
          command = self.getOrientation()

          # If the command is not None and game isn't paused, 
          # send the input Socket command to the server
          if command is not None and paused == False:
            mySocket.send(command.encode("UTF-8"))


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
