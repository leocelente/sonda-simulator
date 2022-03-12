#!/usr/bin/env python3
from Simulator import Simulate
from matplotlib import pyplot as plt
import numpy as np
from nptyping import NDArray
import Air
from Balloon import Balloon

def main():
  state = np.vstack([ 0.0, # altitude
                      0.0 # velocity
  ])
  balloon: Balloon = Balloon()
  tfinal: float = 2 * 60 * 60 
  data, time = Simulate(state, balloon.Model, time_start = 0, time_end = tfinal, time_step=1)
  
  hs = np.linspace(0, 30e3, 1000, dtype=float)

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
  plt.figure()
  plt.subplot(2, 1, 1)
  # plt.ylim([0, 30e3])
  plt.plot(time/60, data[:, 0])
  plt.grid()
  plt.subplot(2, 1, 2)
  plt.plot(time/60, data[:, 1])
  # plt.ylim([0, 1e2])
  plt.grid()

  plt.show()
  

if __name__ == '__main__':
    main()
