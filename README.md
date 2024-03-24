# Tamagotchi-Incubator
## Introduction
An automated Tamagotchi caretaker. I wouldn't recommend trying to remake this project. It takes a lot of work, especially with tuning the vision and setting up the Raspberry Pi to use the LCD, etc. Also the code in this repository is very messy. If you do decide to try the challenge, I wish you the best of luck. Shoot me a message and I'll try to help.

## YouTube video
https://youtu.be/UO_E9Lg-0vo

## 3D models
https://www.printables.com/model/818480

## Instructions
Models can be printed without supports, I used PLA. If you use black material maybe you don't need a shield in the back. I did need this because the backside reflected light into the screen making it hard to do vision. 

As the models are, the camera might not align with the tamagotchi so you need to wedge some material in between.

I used m2 threaded inserts, bolts and nuts for this project. 

Main parts:
- Plexiglass 3mm thickness
- Raspberry Pi 3
- 3.5inch RPi LCD, 480x320, IPS, Resistive Touchscreen
- Raspberry Pi Camera Module 2 - 8MP
- LISIPAROI White LED ring for RPi Camera
- Raspberry Pi GPIO Edge connector(2x40-pins) (for splitting GPIO)
- DSI/CSI Flex cable for Raspberry Pi - 61cm (could have been way shorter)
- 40 pins Rainbow GPIO cable extender male/female - 10cm (I had to use dupont since this was sold out at the time)
- 3x SG90 servo
- Some tiewraps for cable management
- Dupont connectors for Raspberry Pi <-> Light Ring
- I2C PCA9685 12-Bit 16 channel PWM/Servo Driver board

## Electrical schematic
Use the code and parts documentation to figure out what goes where.
