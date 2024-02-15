from transitions import Machine

class TamaStatemachine(object):
  # Define some states
  states = ['unknown', 'egg', 'idle', 'sleeping', 'sick', 'poopy', 'dead',
             'transforming', 'playing', 'eating', 'snacking', 'showing_clock',
               'setting_clock', 'checking_stats']
  
  def __init__(self):
    self.machine = Machine(model=self, states=self.states, initial = 'unknown')
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