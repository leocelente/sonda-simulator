from typing import Callable
import numpy as np
from Integrator import RK4
from Local import *

'''
This is from a previous project, I'm trying to reuse code
'''

def s(progress:float):
  ''' 
  Change this parameter to print the progress
  '''
  pass


def Simulate(state: list[float], model, time_start:float=0, time_end: float=30,  time_step:float=1, status=s):
  '''
  Run simulation of `model` from `time_start` to `time_end`
  '''
  print(f"Simulating from {time_start}s to {time_end}s with dt of {time_step}s")
  time = np.arange(time_start, time_end, time_step, dtype=float)

  view_state = []
  for i in range(len(time)):
      status(i/len(time))
      state = RK4(model, state, time[i], time_step)
      view_state.append(state[:, 0])
  return view_state, time
