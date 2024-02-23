from transitions import Machine
from time import sleep

class TamaCareState(object):
  careStates = ['idle', 'sleeping', 'sick', 'poopy',
             'unhappy', 'hungry', 'undisciplined']
  
  def __init__(self):
    self.machine = Machine(model=self, states=self.careStates, initial = 'idle')

    self.machine.add_transition('play', 'unhappy', 'idle')
    self.machine.add_transition('need_play', 'idle', 'unhappy')
    self.machine.add_transition('eat', 'hungry', 'idle')
    self.machine.add_transition('need_food', 'idle', 'hungry')
    self.machine.add_transition('sleep', 'idle', 'sleeping')
    self.machine.add_transition('wake_up', 'sleeping', 'idle')
    self.machine.add_transition('get_sick', 'idle', 'sick')
    self.machine.add_transition('cure', 'sick', 'idle')
    self.machine.add_transition('poop', 'idle', 'poopy')
    self.machine.add_transition('clean_up', 'poopy', 'idle')
    self.machine.add_transition('misbehave', 'idle', 'undisciplined')
    self.machine.add_transition('discipline', 'undisciplined', 'idle')

class TamaPhysState(object):
  physStates = ['unknown', 'egg', 'baby', 'child', 'teen', 'adult', 
                      'adult_secret', 'dead']
  teenType = 'none'
  adultType = 'none'
  secretAdultType = 'none'

  def __init__(self):
      self.machine = Machine(model=self, states=self.physStates, initial = 'unknown')
      self.machine.add_transition('hatch', 'egg', 'baby')
      self.machine.add_transition('baby_to_child', 'baby', 'child')
      self.machine.add_transition('child_to_teen', 'child', 'teen')
      self.machine.add_transition('teen_to_adult', 'teen', 'adult')
      self.machine.add_transition('adult_to_secret', 'adult', 'adult_secret')
      self.machine.add_transition('die', '*', 'dead')

class TamaController(object):
  def __init__(self, tamaCam, tamaVision, tamaButtons, tamaLog, tamaLight):
    self.tamaCam = tamaCam
    self.tamaVision = tamaVision
    self.tamaButtons = tamaButtons
    self.tamaLog = tamaLog
    self.tamaLight = tamaLight
    self.careState = TamaCareState()
    self.physState = TamaPhysState()

  def getFrame(self, fn):
    self.tamaLight.turnOn()
    sleep(1)
    self.tamaCam.getFrameToFile(fn)
    self.tamaLight.turnOff()
  
  def updateTamaStatFrames(self):
    self.tamaButtons.pressL_nTimes(6)
    self.tamaButtons.pressM()
    self.getFrame('weight_age.jpg')
    self.tamaButtons.pressL()
    self.getFrame('discipline.jpg')
    self.tamaButtons.pressL()    
    self.getFrame('hunger.jpg')
    self.tamaButtons.pressL()
    self.getFrame('happiness.jpg')
    self.tamaButtons.pressR()
    

    unhappy = False
    hungry = False
    return unhappy, hungry

  def checkNeedsDiscipline(self):
    needsDiscipline = False
    return needsDiscipline

  def updateStates(self):
    fn = 'frame.jpg'
    self.getFrame(fn)

    print('Physical state before: ' + self.physState.state)
    self.detectPhysState(fn)
    print('Physical state after: ' + self.physState.state)

    print('Care state before: ' + self.careState.state)
    self.detectCareState(fn)
    print('Care state after: ' + self.careState.state)

  def detectCareState(self, frameFileName):
    if self.tamaVision.findPattern(frameFileName, 'poop1.png'):
      self.careState.to_poopy()  
      return    
    if self.tamaVision.findPattern(frameFileName, 'sick.png'):
      self.careState.to_sick()  
      return
    if self.tamaVision.findPattern(frameFileName, 'sleep.png'):
      self.careState.to_sleep()
      return   
    
    if self.tamaVision.findPattern(frameFileName, 'needs_discipline.png'):
      self.careState.to_undisciplined()
      return
    
    self.updateTamaStatFrames()
    if self.tamaVision.findPattern('hunger.jpg', 'heart_empty.png'):
      self.careState.to_hungry()
      return
  
    if self.tamaVision.findPattern('happiness.jpg', 'heart_empty.png'):
      self.careState.to_unhappy()
      return
    
    print('Tamagotchi seems to not need care right now.')
    self.careState.to_idle()
    return
    
  def detectPhysState(self, frameFileName):
    if self.tamaVision.findPattern(frameFileName, 'angel.png'):
        self.physState.to_dead()  
        return    
    if self.physState.state == 'unknown':
      if self.tamaVision.findPattern(frameFileName, 'egg.png'):
        self.physState.to_egg()
        return
    if self.physState.state in ['unknown', 'egg']:
      if self.tamaVision.findPattern(frameFileName, 'baby.png'):
        self.physState.to_baby()
        return
    if self.physState.state in ['unknown', 'baby']:
      if self.tamaVision.findPattern(frameFileName, 'child.png'):
          self.physState.to_child()
          return
    if self.physState.state in ['unknown', 'child']:
      if self.tamaVision.findPattern(frameFileName, 'teen1.png'):
        self.physState.to_teen()
        self.physState.teenType = 'teen1'
        return
      if self.tamaVision.findPattern(frameFileName, 'teen2.png'):
        self.physState.to_teen()
        self.physState.teenType = 'teen2'
        return
    if self.physState.state in ['unknown', 'teen']:
      if self.tamaVision.findPattern(frameFileName, 'adult1.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult1'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult2.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult2'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult3.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult3'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult4.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult4'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult5.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult5'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult6.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult6'
        return
    if self.physState.state in ['unknown', 'adult']:
      if self.tamaVision.findPattern(frameFileName, 'adult_secret_1.png'):
        self.physState.to_adult_secret()
        self.physState.secretAdultType = 'adult_secret_1'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult_secret_2.png'):
        self.physState.to_adult_secret()
        self.physState.secretAdultType = 'adult_secret_2'
        return
    print('Somehow, no physical state found...')

  def handleState(self):
    if self.physState.state == 'egg':
      print('Waiting for egg to hatch...')
      return

    if self.physState.state == 'dead':
      print('The Tamagotchi is now an angel...')
      return
    
    if self.careState.state == 'idle':
      print('The Tamagotchi is happy and does not need any care')
      return
    
    if self.careState.state == 'poopy':
      print('Cleaning the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(5)
      self.tamaButtons.pressM()
      sleep(3)
    
    if self.careState.state == 'sick':
      print('Healing the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(4)
      self.tamaButtons.pressM()
      sleep(3)

    if self.careState.state == 'hungry':
      print('Feeding the Tamagotchi.')
      self.tamaButtons.pressL()
      self.tamaButtons.pressM()
      self.tamaButtons.pressM()

    if self.careState.state == 'unhappy':
      print('Playing with the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(3)
      self.tamaButtons.pressM()
      sleep(3)
      for i in range(10):
        self.tamaButtons.pressL()
        sleep(1)
      self.tamaButtons.pressR()

    if self.careState.state == 'sleeping':
      print('Turning light off for the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(2)
      self.tamaButtons.pressM()
      self.tamaButtons.pressL()
      self.tamaButtons.pressM()

    if self.careState.state == 'undisciplined':
      print('Disciplining the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(7)
      self.tamaButtons.pressM()

  def getAndHandleState(self):
    self.updateStates()
    self.tamaLight.turnOn()
    self.handleState()
    self.tamaLight.turnOff()