
The objective of this lab was to learn how to deal with analog input/output using an accelerometer, a OLED display, the PMW functionality and a motor. 

For tutorial DisplayI2C, I learned how to use an OLED to display whatever we wished to display. 

For tutorial AnalogInputPart1, we learned how to setup an accelerometer that would detect change in direction in three axes : x,y,z . Serial.plotter would plot the changes of each axis. 

For tutorial AnalogOutputPart1, we learned how to make a LED light up at different intensities. Using a pmw channel, we defined the duty cycle which would set the intensity of the light. 

For tutorial AnalogOutputPart2, we learned how to setup a motor that would buzz according to the intensity that I defined. We did so by settting the duty cycle accordingly while using a pmw channel. 

For tutorial  Sampling, we learned how to setup the arduino to read the analog input coming from the Accelerometer at a specific sample rate. 

## Challenge 1 

We were asked to build a tap gesture detector using the accelerometer. The number of taps would be displayed on the OLED. 

We were told to create a function called "detectTaps()" to detect taps. 

To do that, I observed the changes in ax, ay and az in reaction to taps. So I came to the conclusion that each one of the axes oscillated between a range of values when there was no tap. To get a closer look of these values, I sampled the axes at a sampling rate of 100Hz and printed them out in Serial.monitor. I then annotated the range of values that each axis would take on when there was no tap. 

Inside the detectTaps tab, I created an algorythm that detected a tap whenever two of the axes was out of range. This allowed for detectTaps to not be that sensible to changes in the axes values because otherwise it would recognize every slight change as a tap. 

<img width="697" alt= "DETECT" src="https://user-images.githubusercontent.com/70724215/115501634-69a8e500-a228-11eb-8af2-9b7eea813871.png">

![challenge1](https://user-images.githubusercontent.com/70724215/115502034-2307ba80-a229-11eb-9363-ca44f503972c.gif)




## Challenge 2

We were asked to implement the functionality of a gesture control watch. 
To do so, we will build it as FINITE STATE MACHINE.
Following the requirements for the states, I came up with a state machine that had 3 states: zero_state, counting_state and countdown_state
My watch was detecting the buzzing of the motor as a tap so I wrote the code in a way that only the second tap was detected when state = zero_state
![state machine](IMG_0036.jpg)

File are too long so I put it inside the Images folder 
### Demonstrates the reset functionality 
![reset press](reset.gif)
### Counts to 56 and after 4s go by it counts down to 0

![countdown](countdown.gif)

#### 1 .Starts at zero and counts to 25
#### 2. 4 s go by
#### 3.  Goes to countdown state 
####4. I press before it gets to zero which is when taps:5. It is in counting state.

#### 5. I tap until taps: 18 
#### 6. 4 s go by
#### 7. Counts down to zero

![counts](counts.gif)
