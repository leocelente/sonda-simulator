from numpy import pi 

# Gas Constant R
R = 8.3144598
# Gravity Acceleration
g = 9.80665
# 
M = 0.0289644
BoltzC = 1.38e-23
molar_mass_he = 4.0026e-3 # kg/mol
    

def vol_sphere(radius: float) -> float:
  return (4/3) * pi * radius**3

def radius_sphere(volume:float) -> float:
  return ((3.0/4.0/pi) *volume) ** (1/3)
