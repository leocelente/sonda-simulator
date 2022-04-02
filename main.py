#!/usr/bin/env python3
import sys
from Simulator import Simulate
from matplotlib import pyplot as plt
import numpy as np
from Instrument import probe
from Balloon import Balloon
from Visualization import Viz

def status(percent):
    percent = percent * 100.0
    sys.stdout.write('Progress: \033[K' + ('%.2f' %  percent) + '%\r')

def main():
  state = np.vstack([ 0.0,  # altitude
                      0.0   # velocity
  ])

  balloon = Balloon(balloon_mass=1000,                # 
                              payload_mass=1.8,       #
                              initial_diameter=1.4,   #
                              burst_diameter=8,       #
                              drag_coef=0.35,         #
                              parachute_diameter=1.5, #
                              parachute_drag_coeff=0.6)
  # Simulate for 3 hours
  tfinal: float = 3 * 60 * 60 
  
  data, time = Simulate(state, balloon.Model, time_start = 0, time_end = tfinal, time_step=.5, status=status)
  
  
  # Plot Simulation Data
  data = np.array(data)
  p = probe.get()
  data = np.column_stack((data, p))
  Viz(data, time)
  
if __name__ == '__main__':
    main()
