from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

def Viz(data, time) -> None:
  altitudes =     data[:, 0] * 1e-3
  speed =         data[:, 1]
  volumes =       data[:, 2]
  buoyancy =      data[:, 3]
  drag =          data[:, 4]
  density =       data[:, 5]
  acceleration =  data[:, 6]
  weights =       data[:, 7]
  
  minutes =       time / 60

  plt.figure(figsize=(14, 8))
  plt.title("Simulation Results")

  ax = plt.subplot(3,2,1)
  plt.plot(minutes, altitudes, linewidth=2, color="black")
  plt.legend(["Altiude"])
  plt.ylabel("Altitude [km]")
  plt.grid()

  plt.subplot(3,2,2, sharex=ax)
  plt.plot(minutes, altitudes, linewidth=2, color="black")
  plt.legend(["Altitude"])
  plt.ylabel("Altitude [km]")
  plt.grid()

  plt.subplot(3,2,3, sharex=ax)
  plt.plot(minutes, speed, linewidth=2, color="orange")
  plt.legend(["Ascent Rate"])
  plt.ylabel("Speed [m/s]")
  plt.grid()
  
  plt.subplot(3,2,5, sharex=ax)
  plt.plot(minutes, buoyancy, linewidth=2, color="red")
  plt.plot(minutes, drag, linewidth=2, color="green")
  plt.plot(minutes, weights, linewidth=2, color="yellow")
  plt.legend(["Buoyancy", "Drag", "Weight"])
  plt.ylabel("Force [N]")
  plt.grid()
  plt.xlabel("Time [minutes]")  

  plt.subplot(3,2,4, sharex=ax)
  plt.plot(minutes, acceleration, linewidth=2, color="purple")
  plt.legend(["Acceleration"])
  plt.ylabel("Acceleration [$m/s^2$]")
  plt.grid()

  ax2 = plt.subplot(3,2,6, sharex=ax)
  plt.plot(minutes, volumes, linewidth=2, color="blue")
  plt.legend(["Volume"])
  plt.ylabel("Volume [$m^3$]")
  plt.grid()
  
  ax3 = ax2.twinx()
  ax3.plot(minutes, density, color='cyan', linewidth=2)
  ax3.set_ylabel("Density [$kg/m^3$]")
  plt.xlabel("Time [minutes]")
  
  plt.show()

  

