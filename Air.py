import numpy as np
import Utils

"""
Atmospheric Model

"""

# Atmospheric Pressure Layer Constants
P_sl0 = 101325  # Pa
P_sl1 = 22552   # Pa
P_sl2 = 2481    # Pa

# Atmospheric Density Layer Constants
p_sl0 = 1.225   # kg/m3   
p_sl1 = 0.3629  # kg/m3   
p_sl2 = 0.0399  # kg/m3 

# Helium Gas density at 1 atm and 0C
p_he = 0.1786   # kg/m3

# Atmospheric Temperature Layer Constants
T_sl0 = 288 - 273.15
T_sl2 = 216.5 - 273.15

L_sl0 = -0.0065
L_sl2 = 0.001

# Gas Constant R
R = 8.3144598
# Gravity Acceleration #TODO: move definition to different module
g = 9.80665
# 
M = 0.0289644
BoltzC = 1.38e-23


# Functions
# Based on: https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html

def temperature(altitude: float) -> float:
  '''
  Calculates Temperature in *Kelvin* at certain altitude in meters
  '''
  out: float = 0
  if altitude < 11e3:
    out = 15.04 - 6.49e-3 * altitude
  elif altitude < 25e3:
    out = -56.46
  # elif altitude < 33e3:
  else:
    out = -131.21 + 0.00299 * altitude
    # raise Exception()
  return Utils.kelvin(out)


def pressure(altitude: float) -> float:
  '''
  Calculates air pressure in pascals at altitude in meters
  '''
  out: float = 0
  if altitude < 11e3:
    out = P_sl0 * (temperature(altitude)/288.08)**5.256
  elif altitude < 25e3:
    out = P_sl1 * np.exp((1.73 - 0.000157*altitude))
  # elif altitude < 33e3: 
  else:
    out = P_sl2 * (temperature(altitude)/216.6)**(-11.388)
    # raise Exception(altitude)
  return out


def density(altitude : float) -> float:
  '''
  Calculates the air density in kilogram/cubic meter at altitude in meter
  '''
  P_kpa = pressure(altitude)*1e-3
  K = temperature(altitude)
  p = P_kpa / (.2869 * K)
  if(p > 10):
    print(f"T: {K}K, P: {P_kpa}kPa")
  return p

