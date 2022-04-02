from numpy import pi 
# Gas Constant R
R = 8.3144598
# Gravity Acceleration
g = 9.80665
# 
M = 0.0289644
BoltzC = 1.38e-23
molar_mass_he = 4.0026e-3
    

def vol_sphere(radius: float) -> float:
  return (4/3) * pi * radius**3
