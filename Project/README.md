# Final Project
### **Team: Brenner Lim A15523979, Maria Santos A15616273**

One of the objectives of this lab was to improve a game controller to play the game SpaceInvaders. We used Socket communication to communicate between the game server and the client. We communicated with the MCU using the client file, and the client could communicate with the server via Socket. 
At the end, we implemented an improved game controller with 3 features. 

Our second objective of this lab was to create a New Game Controller from scratch. The game chosen was : Pac-Man.

# The Grand Challenge: Part 1 – Space Invaders Controller
Here, we were given the code for the game and the controller file. The script that ran the game "spaceinvaders.py" acted as the server that connected to the "space_invaders_controller.py" file, via Socket.The "space_invaders_controller.py" file receives and sends data from and to the MCU and acts as the client.
For this part, we were asked to add at least 3 improvements and 3 features to our controller.

Youtube Demo: https://youtu.be/fyA6aVJcuMg

## Controller Improvements
1. The first improvement made was **reducing the noise of the accelerometer by applying an moving average**. By filtering the accelerometer data, we got a clearer signal to pass it through the threshold values. And instead of calculating the orientation on the MCU, we will be calculating the orientation in the client file. 

2. The second improvement was to **decouple the firing and the movement**. In the base controller setup given, the possible orientations were LEFT, RIGHT, UP, and DOWN. Because firing was connected to the vertical direction, the controller couldn't move to the left or right and fire at the same time. Our solution was to add a button that would tell the game to fire. 

    This was implemented by the MCU sending a 1 to the Python client whenever the player wanted to fire by pressing the fire button down and 0's for the remainder of the time. Then the client would send the fire command over Socket communication. The MCU only sends 1 when the pulled-up button is pressed down, or the falling edge. This was done to reduce the amount of commands flooding the Socket communication channel which leads to a buffer of commands which "lags" the game.

3. The last improvement made to the controller was to have **the Python client send controller commands over the Socket channel only when the server is running the actual gameplay rather than the entire time during the menus**. The reason behind this is that the Socket commands are only cleared when the `check_input_udp_socket()` is ran, more specifically `mySocket.recvfrom(1024)`. Whenever this line is ran, the message being received in the Socket channel is saved to be interpreted and cleared from the buffer at the same time. Since this function only lies in gameplay state, commands being sent by the client during the menus will pile up and create a buffer, which will make the controller feel unresponsive as the server has to catch up. Although this buffer issue is reduced by the moving average filter solution slowing down the commands sent during gameplay, the client also has to stop sending commands during the menus. This is done by having the client not send commands over Socket communication until `startGame` is true. 

    This was implemented by having the Space Invaders server send the "START" command to the client whenever the enter key is pressed to start the game during the main menu. When the player loses all of their lives, the server will send "END" to the client, telling the client to stop Socket commands.
    

``` python
''' The while loop that runs the game'''
    def main(self):
        while True:
            if self.mainScreen:

                ''' ===================================================== '''
                # This block of code lets the game save the address of the controller
                # for future Socket commands while in the Main Menu
                # Clears up buffer for any junk commands if any
                try:
                    ___, self.addr = mySocket.recvfrom(1024)
                except BlockingIOError:
                    pass
                ''' ===================================================== '''
                ....
                
                for e in event.get():
                    if self.should_exit(e):
                        sys.exit()
                    if e.type == KEYUP:
                        ....
                        ''' ===================================================== '''
                        # Tells controller client that game is started
                        mySocket.sendto("START".encode('utf-8'),self.addr)
                        ''' ===================================================== '''
                        ....

            elif self.startGame:
                ....

            elif self.gameOver:
                ....
                
                ''' ===================================================== '''
                # Tell client to stop sending Socket commands while in Game Over screen
                mySocket.sendto("END".encode('utf-8'),self.addr)
                ''' ===================================================== '''
                ....
```

## Controller Features

1. **Buzzing and OLED Feedback:** This feature utilizes the motor and OLED in order to buzz and display "SHOT" whenever the player is hit in the game. This is done by having the server send "BUZZ" whenever the game detects a bullet colliding with the player. 
   This is then received by the client that then tells the MCU controller to activate the motor and display "SHOT" on the OLED display.

``` python
''' When inside the while loops while the controller is running '''
    while True:
      ....
      # Check if server sends any commands (START,END,BUZZ)
      try: 
        data = mySocket.recv(1024).decode("utf-8")
      except BlockingIOError:
        pass

      # Tells MCU to vibrate when player is hit
      if data == "BUZZ":
        self.comms.send_message("BUZZ")
        data = None
      ....

```

2. **OLED Interface:** This feature displays the current score. This is done by repeatingly sending the current score value to the client. If the client sees that the score has changed, it will send the new score to the MCU to update the OLED.

    Since the commands sent by the server can only be "START", "END", and "BUZZ", we just use an if statement such that if the Socket data isn't `None` or isn't any of the other 3 commands, then it must be the current score. We save the score locally in the client to check if the current score has changed before telling the MCU to update the OLED.

``` python
    while True:
      ....
      # Check if server sends any commands (START,END,BUZZ)
      try: 
        data = mySocket.recv(1024).decode("utf-8")
      except BlockingIOError:
        pass

      # Tells MCU to vibrate when player is hit
      if data == "BUZZ":
        ....

      # Sends score to MCU to display on OLED if score has changed
      elif data != "END" and data != "START" and data != None:
        if score != int(data):
          score = int(data) # Updates local score to current
          self.comms.send_message(f"{score}")
      ....
```

3. **Pause/Resume Functionality:** This functionality allowed for the player to pause and resume the game by using a second button. 
   Whenever a "PAUSE" command was received by the client (from MCU), the client would send the command to the server and the server would pause the game. We did that by having a while loop run that only updates the game timers when "PAUSE" is sent again. By doing that, the game components and positions will remain in place after we press pause again. 
   In order to implement this functionality, we created a new method called "pauseGame" that runs a while loop until we receive another "PAUSE" to resume the game. In client, we use a boolean variable called "paused" to keep track of when the game is paused. 
   It happens as follows : when we press the pause button, the MCU sends a 1 to client which sets 'paused' to True and sends "PAUSE" to the server. 

    
``` python
    ''' ===================================================== '''
    def pauseGame(self):
        while True:
            # Updating the timers so game doesn't speedup after unpausing
            self.timer = time.get_ticks() # Game timer
            self.enemies.timer = time.get_ticks() # Enemy Movement Timer
            if self.timer - self.noteTimer > self.enemies.moveTime:
                self.noteTimer += self.enemies.moveTime # Note Timer

            # Loops until server receives "PAUSED" command
            try:
                data, __ = mySocket.recvfrom(1024)
                data = data.decode('utf-8')
                if data == "PAUSE":
                    data = None
                    break
            except BlockingIOError:
                pass
            # Blocks game until 60 ticks have passed for this loop (essentially update speed)
            self.clock.tick(60)
    ''' ===================================================== '''
```

# Instructions to SpaceInvaders Controller
1. Upload the Arduino sketch  in ece16-space-invaders/controller/Arduino (You might wish to callibrate the zero values of the accelerometer data)

2. Run spaceinvaders.py in ece16-space-invaders/SpaceInvaders and space_invaders_controller.py in ece16-space-invaders/controller/Python in two separate terminals

3. Once "Ready to start? Hit enter to begin" appears in the controller terminal, press Enter.

4. With the SpaceInvaders game window opened, press any key to start the game.

5. In case you wish to pause the game, press one of the buttons on the MCU

6. To fire, press the second button on the MCU

7. Tilt the controller to the left or right to move accordingly.


# The Grand Challenge: Part 2 – PacMan Controller

For part 2, we uploaded a pacman game server from the internet and created the file "pacman_controller.py" for the controller. We used "space_invaders_controller.py" as a base to write the code for "pacman_controller.py".
Youtube Demo: https://youtu.be/qlBma1vwDjw

## Controller Features

1. **Tilt Controls:** Our Pacman controller has separate variables for horizontal and vertical directions, which means that we can also do diagonal moves. 

To implement this, we also took the moving average of the accellerometer data in order to read the moves more accurately. 

2. **OLED Display** We got our OLED to display the score and the number of lives. And once we've run out of lives, we get it to display "Game Over".

3. **Buzzing** We also got our controller to vibrate whenever we touch a ghost.


# Controller Design
Our controller uses essentially the same features and improvements that we used for SpaceInvaders. Our goal was to implement these changes using this new game server code which presented new challenges for our design.  

1. The first point is the fact that commands in the Socket channel are only cleared when the server runs `mySocket.recvform(1024)`. If this isn't ran continuously while the game is running, a buffer of commands from the Socket client will render the controller useless. By having this line ran continuously in the loop, this problem can be avoided. This made the `gameStart` boolean variable in Space Invaders controller code to tell the client to stop sending Socket commands redundant in the Pac-Man controller code.

    *Python Code: Reading message from Socket channel in Server *
    ``` python
    while True: 

    CheckIfCloseButton( pygame.event.get() )

    ''' ============================================================ '''
    # Checks continuously for Socket commands by client while the game is running
    try:
        msg, ___ = mySocket.recvfrom(1024) # receive 1024 bytes
        msg = msg.decode('utf-8')
        print("Command: " + msg)
    except BlockingIOError:
        pass
    ''' ============================================================ '''
    ....
    ```

2. We created a separate function that was used to handle user inputs from the UDP client. In pacman.pyw, we created the function `CheckInputs_udp_sockets()` in the `game` class to handle the user input messages and move the player accordingly. The messages are being collected outside of this function, so we need to call this function with the message that we received from client. 

    *Python Code: Checking User Inputs from Socket channel in Server*
    ``` python
    # New function that looks for inputs via controller 
    def CheckInputs_udp_sockets(msg):

        if thisGame.mode == 1:
            if msg == "RIGHT":
                if not thisLevel.CheckIfHitWall(player.x + player.speed, player.y, player.nearestRow, player.nearestCol): 
                    player.velX = player.speed
                    player.velY = 0
                    
            elif msg == "LEFT":
                if not thisLevel.CheckIfHitWall(player.x - player.speed, player.y, player.nearestRow, player.nearestCol): 
                    player.velX = -player.speed
                    player.velY = 0
            elif msg == "DOWN":
                if not thisLevel.CheckIfHitWall(player.x, player.y + player.speed, player.nearestRow, player.nearestCol): 
                    player.velX = 0
                    player.velY = player.speed
                
            elif msg == "UP":
                if not thisLevel.CheckIfHitWall(player.x, player.y - player.speed, player.nearestRow, player.nearestCol):
                    player.velX = 0
                    player.velY = -player.speed
                    
        if pygame.key.get_pressed()[ pygame.K_ESCAPE ] or msg == "QUIT":
            sys.exit(0)
                
        elif thisGame.mode == 3:
            if pygame.key.get_pressed()[ pygame.K_RETURN ] or (js!=None and js.get_button(JS_STARTBUTTON)):
                thisGame.StartNewGame()
    ```

3. The last thing to note was that when wanting to send commands to the controller, we have to first get the address of the client.  
    In Pac-Man this was implemented by having a while loop that will freeze the game until the controller begins to run after an "enter" key.

    *Python Code: While loops waiting for controller startup in Server*
    ``` python
    ....
    ''' ============================================================ '''
    # Initialize msg variable to hold Socket commands
    msg = None

    # Loop checks for the start message of the controller client for the address
    while True:

        # Looks for msg
        try:
            msg, addr = mySocket.recvfrom(1024) # receive 1024 bytes
            msg = msg.decode('utf-8')
            print("Command: " + msg)

            if msg == "CONTROLLER":
                break
        except BlockingIOError:
            pass
    ''' ============================================================ '''
    ....
    ```
   
# Instructions to Pac-Man Controller
1. Upload the Arduino sketch PacManController in Design Challenge/controller/Arduino,

2. Run pacman.pyw in Design Challenge/pacman-python/pacman and pacman_controller.py in Design Challenge/controller/Python* in two separate terminals

3. Once "Ready to start? Hit enter to begin" appears in the controller terminal, press Enter.

4. With the pacman game window opened, press "Enter" to start the game.

5. In case you wish to pause the game, press the button on the MCU.

6. You can move to the left, right, up, down  and diagonally by tilting the controller
