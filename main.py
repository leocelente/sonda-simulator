#!/usr/bin/env python3
import time as t
import sys
import numpy as np
from Simulator import Simulate
from Instrument import probe
from Balloon import Balloon
from Visualization import Viz


def status(progress: float) -> None:
    progress = progress * 100.0
    sys.stdout.write('Progress: \033[K' + ('%.2f' % progress) + '%\r')


def main():

    print("-- Started Simulation --")

    # Simulate for 3 hours
    tfinal: float = 3 * 60 * 60
    time_str = t.strftime("%Hh%Mm%Ss", t.gmtime(tfinal))

    print(f"Duration: {time_str}")

    models = {'Kaymond 3000': {"mass": 3000, "burst_d": 13.0},
              'Kaymond 2000': {"mass": 2000, "burst_d": 10.5},
              'Kaymond 1000': {"mass": 1000, "burst_d": 7.86}
              }
    model = "Kaymond 3000"
    balloon = Balloon(balloon_mass=models[model]["mass"],                #
                      payload_mass=3,       #
                      initial_volume=8,   #
                      burst_diameter=models[model]["burst_d"],       #
                      drag_coef=0.35,         #
                      parachute_diameter=1.5,
                      parachute_drag_coeff=0.6)

    state = np.vstack([0.0,  # velocity
                       0.0,   # acceleration
                       balloon.initial_m_gas  # gas mass
                       ])

    data, time = Simulate(state, balloon.Model, time_start=0,
                          time_end=tfinal, time_step=.5, status=status)

    # Plot Simulation Data
    data = np.array(data)
    # Join probed data
    data = np.column_stack((data, probe.get()))

    Viz(data, time)


if __name__ == '__main__':
    main()
