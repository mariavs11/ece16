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

    x_avg = filt.moving_average(np.array(self.x),5)
    y_avg = filt.moving_average(np.array(self.y),5)
    z_avg = filt.moving_average(np.array(self.z),5)

    x = x_avg[-1]
    y = y_avg[-1]
    z = z_avg[-1]

    # This then checks for left-right and up-down movement
    # if abs(x) >= abs(y) and abs(x) >= abs(z):
    if abs(x) >= 100:
        if x < 0:
            command_hori = "LEFT"
        else:
            command_hori = "RIGHT"
    else:
      command_hori = None

    # elif abs(y) >= abs(x) and abs(y) >= abs(z):
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

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # Sending to give game the address
    mySocket.send("CONTROLLER".encode("UTF-8"))

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")

    # gameStart = False
    gameStart = True
    data = None
    paused = False
    # prevCommand_vert = None
    # prevCommand_hori = None
    prevCommand = None
    
    sleep(1)

    previousTime = time()
    while True:
      message = self.comms.receive_message()

      # Check if server sends any commands (START,END,HIT)
      try: 
        data = mySocket.recv(1024).decode("utf-8")
      except BlockingIOError:
        pass

      # Tells MCU to vibrate when hit
      if data == "HIT":
        self.comms.send_message("BUZZ")
        data = None

      # Sends score to MCU to display on OLED
      elif data != "END" and data != "START" and data != None:
        if score != int(data):
          score = int(data)
          self.comms.send_message(f"{score}")

      # When the game starts, start sending the commands from MCU to game
      if gameStart == False and data == "START":
        gameStart = True
        score = None
        self.comms.clear()
        data = None
      
      # While the game is running, determine controller commands and send to game
      elif(message != None):
        command_hori = None
        command_vert = None
        # message = int(message)

        [m1, m2, m3, m4, m5] = message.split(',')
        # Format: x, y, z, fire binary, pause binary

        # Add to Circularlist
        self.x.add(int(m1))
        self.y.add(int(m2))
        self.z.add(int(m3))

        # Send FIRE command to sever if button was pressed
        if int(m4) == 1:
          mySocket.send("FIRE".encode("UTF-8"))

        # Tells game to pause if pause button was pressed
        if int(m5) == 1:
          mySocket.send("PAUSE".encode("UTF-8"))
          print("Sent pause")
          if paused == True:
            paused = False
          else:
            paused = True

        # After certain time, filter the moving average
        currentTime = time()
        if (currentTime - previousTime >= 0.01):
          previousTime = currentTime
          # print("processing")
          # print(self.x,self.y,self.z)
          command_hori, command_vert = self.getOrientation()

        print(command_hori, command_vert)

        # If the command is not None and the game isn't paused, send the input to the server
        # Sends the command only if the direction has changed
        if paused == False:
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
