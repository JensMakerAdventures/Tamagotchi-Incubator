from time import sleep
import tkinter as tk
from tkinter import messagebox
import os
from picamera import PiCamera
from adafruit_servokit import ServoKit
from transitions import Machine

class Tamagotchi(object):
  # Define some states
  states = ['unknown', 'egg', 'idle', 'sleeping', 'sick', 'poopy', 'dead',
             'transforming', 'playing', 'eating', 'snacking', 'showing_clock',
               'setting_clock', 'checking_stats']
  
  def __init__(self):
    self.machine = Machine(model=self, states=Tamagotchi.states, initial = 'unknown')
    self.machine.add_transition('play', 'idle', 'playing')
    self.machine.add_transition('done playing', 'playing', 'idle')
    self.machine.add_transition('eat', 'idle', 'eating')
    self.machine.add_transition('done_eating', 'eating', 'idle')
    self.machine.add_transition('snack', 'idle', 'snacking')
    self.machine.add_transition('done_snacking', 'snacking', 'idle')
    self.machine.add_transition('lost_state', '*', 'unknown')
    self.machine.add_transition('found_state', 'unknown', '*')
    self.machine.add_transition('hatch_egg', 'egg', 'idle')
    self.machine.add_transition('sleep', 'idle', 'sleeping')
    self.machine.add_transition('wake_up', 'sleeping', 'idle')
    self.machine.add_transition('get_sick', 'idle', 'sick')
    self.machine.add_transition('get_cured', 'sick', 'idle')

    self.machine.add_transition('poop', 'idle', 'poopy')
    self.machine.add_transition('clean_poop', 'poopy', 'idle')
    self.machine.add_transition('die', '*', 'dead')
    self.machine.add_transition('resurrect', 'dead', 'egg')
    self.machine.add_transition('transform', '*', 'transforming')
    self.machine.add_transition('done_transforming', 'transforming', 'idle')
    self.machine.add_transition('show_clock', ['idle', 'sick', 'poopy', 'egg', 'sleeping'], 'showing_clock')
    self.machine.add_transition('set_clock', 'showing_clock', 'setting_clock')
    self.machine.add_transition('back_to_clock', 'setting_clock', 'showing_clock')


class TamaButton:
  def __init__(self, label, channel, retractAngle, activateAngle):
    self.label = label
    self.channel = channel
    self.retractAngle = retractAngle
    self.activateAngle = activateAngle

  def press(self):
    kit.servo[self.channel].angle = self.activateAngle
    sleep(0.5)
    kit.servo[self.channel].angle = self.retractAngle
    sleep(0.5)

buttonL = TamaButton("left", 0, 100, 75)
buttonM = TamaButton("middle", 1, 110, 75)
buttonR = TamaButton("right", 2, 60, 95)

# Servo's
kit = ServoKit(channels=16)

#buttonL.press()
#buttonM.press()
#buttonR.press()
'''
camera = PiCamera()
#camera.resolution = (800, 600)
camera.framerate = 15
camera.start_preview()
sleep(5)
camera.capture('test.jpg')
camera.stop_preview()
'''

# check if display env variable is ok
if os.environ.get('DISPLAY','') == '':
    #print('No $DISPLAY env variable, so using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

gui = tk.Tk()
#gui.geometry("480x320")
gui.attributes('-fullscreen',True)

gui.title("Tamagotchi-Incubator")

def pushButtonCallback(button):
  #msg=messagebox.showinfo( "Hello Python", "Hello World")
  button.press()

B = tk.Button(gui, text ="Push L", command = lambda: pushButtonCallback(buttonL))
B.place(x=50,y=50)

gui.mainloop()