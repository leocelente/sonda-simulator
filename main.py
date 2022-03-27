#!/usr/bin/env python3
from Simulator import Simulate
from matplotlib import pyplot as plt
import numpy as np
import Air
from Balloon import Balloon

def main():
  state = np.vstack([ 0.0, # altitude
                      0.0 # velocity
  ])
  balloon: Balloon = Balloon()
  balloon.burst = False
  tfinal: float = 3 * 60 * 60 
  data, time = Simulate(state, balloon.Model, time_start = 0, time_end = tfinal, time_step=1)
  
  hs = np.linspace(0, 35e3, 1000, dtype=float)

  # Plot individual Models
  Ps = [Air.pressure(h) for h in hs]
  Ts = [Air.temperature(h) for h in hs]
  ps = [Air.density(h) for h in hs]
  Vs = [balloon.volume(h) for h in hs]
  pbs = [balloon.density(h) for h in hs]
  
  plt.subplot(1, 5, 1)
  plt.plot(Ps,hs)  
  plt.legend(["Pressure"])
  plt.grid()
  
  plt.subplot(1, 5, 2)
  plt.plot(Ts,hs)
  plt.legend(["Temperature"])
  plt.xlim([200,280])
  plt.grid()
  
  plt.subplot(1, 5, 3)
  plt.plot(Vs, hs)
  plt.legend(["Balloon Volume"])
  plt.grid()
  
  plt.subplot(1, 5, 4)
  plt.plot( ps, hs)
  plt.legend(["Density"])
  plt.grid()
  
  plt.subplot(1, 5, 5)
  plt.plot(pbs, hs)
  plt.legend(["Balloon Density"])
  plt.grid()
  
  # Plot Simulation Data
  data = np.array(data)
  fig = plt.figure()
  fig.tight_layout(h_pad=2)
  plt.subplot(2, 1, 1)
  plt.title("Altitude")
  plt.ylim([0, 35e3])
  plt.plot(time/60, data[:, 0])
  plt.ylabel("Altitude (m)")
  plt.xlabel("Time (min)")
  plt.grid()
 
  plt.subplot(2, 1, 2)
  plt.title("Ascent Rate")
  plt.plot(time/60, data[:, 1])
  plt.ylabel("Speed (m)")
  plt.xlabel("Time (min)")
  plt.ylim([-30, 20])
  plt.grid()

  plt.show()
  

if __name__ == '__main__':
    main()
