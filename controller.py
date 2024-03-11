from transitions import Machine
from time import sleep
import time
import logging

logger = logging.getLogger('Tamagotchi')

class TamaCareState(object):
  careStates = ['idle', 'sleeping', 'sick', 'poopy',
             'unhappy', 'hungry', 'undisciplined']
  
  def __init__(self):
    self.machine = Machine(model=self, states=self.careStates, initial = 'unknown')
    
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
  def __init__(self, tamaCam, tamaVision, tamaButtons, tamaLight, careInterval, lock):
    self.tamaCam = tamaCam
    self.tamaVision = tamaVision
    self.tamaButtons = tamaButtons
    self.tamaLight = tamaLight
    self.careState = TamaCareState()
    self.physState = TamaPhysState()
    self.amountHunger = 0
    self.amountUnhappy = 0
    self.careInterval = careInterval
    self.lastCare = time.time() - self.careInterval - 1 # Subtract this so you can do the first check straight away
    self.prevLoveMode = True
    self.prevAutoMode = False
    self.SnackKillCounter = 0
    self.lock = lock

  def getFrame(self, fn):
    self.tamaLight.turnOn()
    sleep(0.5)
    with self.lock:
      self.tamaCam.getFrameToFile(fn)
    self.tamaLight.turnOff()
    sleep(0.3)
  
  def updateTamaStatFrames(self):
    self.tamaButtons.pressL_nTimes(6)
    self.tamaButtons.pressM()

    fileNames = ('weight_age.jpg', 'discipline.jpg', 'hunger.jpg', 'happiness.jpg')
    for fn in fileNames:
      self.getFrame(fn)
      self.tamaButtons.pressL()
    self.tamaButtons.pressR()
    self.tamaButtons.pressR()

  def checkNeedsDiscipline(self):
    needsDiscipline = False
    return needsDiscipline

  def detectCareState(self, frameFileName):
    logger.log(logging.WARNING,('Detecting care needs: poop, sickness and sleeping.'))
    if self.tamaVision.findPattern(frameFileName, patternFileNames = ['poop1.png', 'poop2.png']):
      self.careState.to_poopy()
      return    
    if self.tamaVision.findPattern(frameFileName, 'sick.png'):
      self.careState.to_sick()  
      return
    if self.tamaVision.findPattern(frameFileName, patternFileNames=['sleep_1.png', 'sleep_2.png'], positiveThresholds = [0.6, 0.6]):
      self.careState.to_sleeping()
      return

    logger.log(logging.WARNING,('Retrieving stats: age, hunger, happiness and discipline'))
    self.updateTamaStatFrames()

    self.amountHunger = self.tamaVision.findMissingHearts('hunger.jpg', 'heart_empty.png')
    self.amountUnhappy = self.tamaVision.findMissingHearts('happiness.jpg', 'heart_empty.png')
    logger.log(logging.WARNING,('Hunger: Found ' + str(self.amountHunger) + ' hearts missing'))
    logger.log(logging.WARNING,('Happiness: Found ' + str(self.amountUnhappy) + ' hearts missing'))
    if self.amountHunger > 0:
      self.careState.to_hungry()
      return
  
    if self.amountUnhappy > 0:
      self.careState.to_unhappy()
      return

    logger.log(logging.WARNING,('Tamagotchi is OK, does it call for discipline?.'))
    # only check discipline after all other care request have been handled
    if self.tamaVision.findPattern(frameFileName, 'needs_discipline.png', positiveThresholds = 0.85):
      logger.log(logging.WARNING,('Yes!'))
      self.careState.to_undisciplined()
      return
    logger.log(logging.WARNING,('No.'))
    logger.log(logging.WARNING,'Tamagotchi seems to not need care right now.')
    self.careState.to_idle()
    return
    
  def detectPhysState(self, frameFileName):
    logger.log(logging.WARNING,'Detecting physical form.')
    if self.tamaVision.findPattern(frameFileName, 'angel.png'):
        self.physState.to_dead()  
        return    
    self.physState.to_child()
    return
    if self.physState.state in ['unknown', 'dead']:
      if self.tamaVision.findPattern(frameFileName, 'egg_1.png'):
        self.physState.to_egg()
        return
      if self.tamaVision.findPattern(frameFileName, 'egg_2.png'):
        self.physState.to_egg()
        return
    if self.physState.state in ['unknown', 'egg']:
      if self.tamaVision.findPattern(frameFileName, 'baby_1.png'):
        self.physState.to_baby()
        return
      if self.tamaVision.findPattern(frameFileName, 'baby_2.png', positiveThresholds = 0.53):
        self.physState.to_baby()
        return
    if self.physState.state in ['unknown', 'baby']:
      if self.tamaVision.findPattern(frameFileName, 'child_1.png'):
          self.physState.to_child()
          return
      if self.tamaVision.findPattern(frameFileName, 'child_2.png'):
        self.physState.to_child()
        return
      if self.tamaVision.findPattern(frameFileName, 'child_3.png'):
        self.physState.to_child()
        return
    if self.physState.state in ['unknown', 'child']:
      if self.tamaVision.findPattern(frameFileName, 'teen1_1.png'):
        self.physState.to_teen()
        self.physState.teenType = 'teen1'
        return
      if self.tamaVision.findPattern(frameFileName, 'teen1_2.png'):
        self.physState.to_teen()
        self.physState.teenType = 'teen1'
        return
      if self.tamaVision.findPattern(frameFileName, 'teen2_1.png'):
        self.physState.to_teen()
        self.physState.teenType = 'teen2'
        return
      if self.tamaVision.findPattern(frameFileName, 'teen2_2.png'):
        self.physState.to_teen()
        self.physState.teenType = 'teen2'
        return
    if self.physState.state in ['unknown', 'teen']:
      if self.tamaVision.findPattern(frameFileName, 'adult1_1.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult1'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult1_2.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult1'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult2_1.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult2'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult2_2.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult2'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult2_3.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult2'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult3_1.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult3'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult3_2.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult3'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult3_3.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult3'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult4_1.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult4'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult4_2.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult4'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult5_1.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult5'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult5_2.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult5'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult5_3.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult5'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult6_1.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult6'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult6_2.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult6'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult6_3.png'):
        self.physState.to_adult()
        self.physState.teenType = 'adult6'
        return
    if self.physState.state in ['unknown', 'adult']:
      if self.tamaVision.findPattern(frameFileName, 'adult_secret_1_1.png'):
        self.physState.to_adult_secret()
        self.physState.secretAdultType = 'adult_secret_1'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult_secret_1_2.png'):
        self.physState.to_adult_secret()
        self.physState.secretAdultType = 'adult_secret_1'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult_secret_2_1.png'):
        self.physState.to_adult_secret()
        self.physState.secretAdultType = 'adult_secret_2'
        return
      if self.tamaVision.findPattern(frameFileName, 'adult_secret_2_2.png'):
        self.physState.to_adult_secret()
        self.physState.secretAdultType = 'adult_secret_2'
        return
    logger.log(logging.WARNING,'No physical form found...')

  def handleState(self):
    if self.physState.state == 'egg':
      logger.log(logging.WARNING,'Waiting for egg to hatch...')
      return

    if self.physState.state == 'dead':
      logger.log(logging.WARNING,'The Tamagotchi is now an angel...')
      return
    
    if self.careState.state == 'idle':
      logger.log(logging.WARNING,'The Tamagotchi is happy and does not need any care')
      return
    
    if self.careState.state == 'poopy':
      logger.log(logging.WARNING,'Cleaning the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(5)
      self.tamaButtons.pressM()
      sleep(5)
      self.tamaButtons.pressR()
    
    if self.careState.state == 'sick':
      logger.log(logging.WARNING,'Healing the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(4)
      self.tamaButtons.pressM()
      sleep(5)
      self.tamaButtons.pressR()

    if self.amountHunger > 0:
        logger.log(logging.WARNING,'Feeding the Tamagotchi.')
        self.tamaButtons.pressL()
        self.tamaButtons.pressM() #open food menu

        fn = 'frame.jpg'
        self.getFrame(fn)
        if not self.tamaVision.mealSelected(fn): # select nutricious food, our tama must not eat snacks
          self.tamaButtons.pressL()

        while self.amountHunger > 0:
          self.tamaButtons.pressM()
          sleep(7)
          self.amountHunger = self.amountHunger - 1
        self.tamaButtons.pressR()
        self.tamaButtons.pressR()

    if self.amountUnhappy > 0:
      logger.log(logging.WARNING,'Playing with the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(3)
      self.tamaButtons.pressM()
      sleep(5)
      while self.amountUnhappy > 0:
        for j in range(2): #always play 2 games, since you might not win every one
          for i in range(5): # a game has 5 rounds
            self.tamaButtons.pressL()
            sleep(5)
          sleep(8)
        self.amountUnhappy = self.amountUnhappy - 1
      self.tamaButtons.pressR()
      self.tamaButtons.pressR()

    if self.careState.state == 'sleeping':
      logger.log(logging.WARNING,'Turning light off for the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(2)
      self.tamaButtons.pressM()
      self.tamaButtons.pressL()
      self.tamaButtons.pressM()
      sleep(4)
      self.tamaButtons.pressR()

    if self.careState.state == 'undisciplined':
      logger.log(logging.WARNING,'Disciplining the Tamagotchi.')
      self.tamaButtons.pressL_nTimes(7)
      self.tamaButtons.pressM()
      sleep(5)
      self.tamaButtons.pressR()

  def checkIfTamaIsDead(self):
    fn = 'frame.jpg'
    self.getFrame(fn)
    if self.tamaVision.findPattern(fn, 'angel.png'):
      self.physState.to_dead() 
      return True 
    else:
      logger.log(logging.WARNING,'Tamagotchi is not dead yet.')
      return False
    
  def feedSnack(self):
    self.tamaButtons.pressM()
    self.SnackKillCounter += 1
    logger.log(logging.WARNING,'Snacks given: '+ str(self.SnackKillCounter))
    sleep(1)
    self.tamaButtons.pressL()


  def getAndHandleState(self, autoMode, loveMode):
    if autoMode:
      if self.prevAutoMode == False:
        logger.log(logging.WARNING, 'Automatic control enabled...')
      if loveMode:
        if self.prevLoveMode == False:
          logger.log(logging.WARNING,'Good thing you disabled murder mode. You are still a bad person for even trying it...')
        timeSinceLastCare = int(time.time() - self.lastCare)
        #logger.log(logging.WARNING,'Seconds since last care: ' + str(timeSinceLastCare))
        if timeSinceLastCare > self.careInterval:
          self.lastCare = time.time()
          fn = 'frame.jpg'
          self.getFrame(fn)
          self.detectPhysState(fn)

          logger.log(logging.WARNING,'Detected physical state is: ' + self.physState.state)

          if self.physState.state == 'egg':
            logger.log(logging.WARNING,'Not checking care needs, because tama is egg')
            return

          if self.physState.state == 'dead':
            logger.log(logging.WARNING,'Not checking care needs, because tama is dead')
            return

          self.detectCareState(fn)
          logger.log(logging.WARNING,'Care state: ' + self.careState.state)

          self.tamaLight.turnOn()
          self.handleState()
          self.tamaLight.turnOff()
        else:
          sleep(30)
      else: #kill the tamagotchi by feeding it snacks over and over
        if self.prevLoveMode == True:
          logger.log(logging.WARNING,'Tamagotchi murder mode activated. You monster.')
          self.snackKillCounter = 0
          fn = 'frame.jpg'
          self.getFrame(fn)
          self.detectPhysState(fn)

        if self.physState != 'dead':
          self.tamaButtons.pressL()
          self.tamaButtons.pressM()

          fn = 'frame.jpg'
          self.getFrame(fn)
          if self.tamaVision.mealSelected(fn):
            self.tamaButtons.pressL()
          
          i = 0
          while self.physState not in ['dead']:
            self.feedSnack()
            i = i + 1
            if i > 10:
              self.checkIfTamaIsDead()
              i = 0
            
          logger.log(logging.WARNING,'Sweet little Tama is dead. Is this what you wanted??')

      self.prevLoveMode = loveMode   
    self.prevAutoMode = autoMode      
    
    
      