from cmath import isinf, isnan
from shutil import ExecError
import numpy as np
import Air
from Air import g, BoltzC, R
from Universe import vol_sphere
'''
Mass:           Kilogram
Preassure:      Pascal
Temperature:    Kelvin
Altitude:       meter
Force:          Newton
Time:           seconds
Density:        Kg/m^3
Volume:         m^3
Acceleration:   m/s^2
'''

class Balloon():
  # Payload Mass 
  m_payload: float = 2
  # Balloon Mass
  m_balloon: float = 1.0

  # Balllon Initial Radius
  r_i: float = 1.4 / 2 # m
  # Balllon Burst Radius
  r_f: float = 8.0 / 2 # m
  # Balllon Drag Coefficient
  drag_coeff = 0.35
  burst: int = 0

  def volume(self, altitude: float) -> float:
    '''
    Calculates (simplified) the balloon's volume in cubic meters at altitude in meters
    '''
    if(self.burst >= 4):
      return 0

    burst_vol: float = vol_sphere(self.r_f)
    vol: float = self.mass() / (Air.density(altitude) - self.density(altitude)) 
    if vol > burst_vol: # in theory this condition means burst
      self.burst += 1
    return vol

  def density(self, altitude: float) -> float:
    '''
    Calculates the balloon's internal gas density in kilogram per cubic meter at altitude in meters
    '''    
    if(self.burst >= 4):
      return 0
    molar_mass_he = 4.0026e-3
    temperature: float = Air.temperature(altitude) #! Assumption
    pressure: float = Air.pressure(altitude) #! Assumption
    density: float = pressure / (R / molar_mass_he * temperature)  
    return density


  def drag(self, altitude: float, velocity: float) -> float:
    '''
    Calculates the drag force at altitude in meters while moving at velocity in meters per second
    '''
    if(self.burst >= 4): 
      self.drag_coeff = 0.65
      area = np.pi * 1.5**2
    else: 
      radius = ((3.0/4.0/np.pi) * self.volume(altitude)) ** (1/3)
      area: float = np.pi * radius * radius
    d: float = -(1/2) * self.drag_coeff * Air.density(altitude) * area * (abs(velocity)*velocity)
    if(isnan(d) or isinf(d) or abs(d) > 100):
      print(f"Cd: {self.drag_coeff}, rho_a: {Air.density(altitude)}, A: {area}, v: {velocity}, v2: {abs(velocity)*velocity}")
      raise RuntimeError()
    return d


  def mass(self):
    # Expected Helium Mass 
    m_gas: float =  vol_sphere(self.r_i) * self.density(0)
    if(self.burst >= 4):
        self.m_balloon = 0
        m_gas = 0
    mass: float = self.m_payload + self.m_balloon + m_gas
    return mass


  def weight(self) -> float:
    '''
    Total Weight
    '''
    return -self.mass() * g


  def buoyancy(self, altitude: float) -> float:
    '''
    Calculates the Buoyancy force at a given altitude
    '''
    if(self.burst >= 4):
      return 0
    return g * self.volume(altitude) * Air.density(altitude)


  def acceleration(self, altitude: float, velocity: float) -> float:
    '''
    Calculates the acceleration in meters per second square from altitude and (previous dt) velocity
    '''
    acc: float  = (self.buoyancy(altitude) + self.weight() + self.drag(altitude, velocity)) / self.mass()
    if(acc < -11):
      print(f"B: {self.buoyancy(altitude)}, W: {self.weight()}, D: {self.drag(altitude, velocity)}, rho_a: {Air.density(altitude)}")
      # raise RuntimeWarning()
    return acc


  _i = 0
  def Model(self, t: float, state: list[list[float]]):
    '''
    Calculates the derivative (delta state) to be integrated on simulation step
    '''
    current_altitude: float  = state[0][0]          # altitude
    current_velocity: float  = state[1][0]          # velocity
    
    delta  = np.vstack([ current_velocity, # altitude
                        self.acceleration(current_altitude, current_velocity) # velocity
    ])

    # Convenience variables for debugging
    vol: float = self.volume(current_altitude)
    rho: float = self.density(current_altitude)
    buoy: float = self.buoyancy(current_altitude)
    drag: float = self.drag(current_altitude, current_velocity)
    weight: float = self.weight()
    mass: float = self.mass() 
    acc: float = self.acceleration(current_altitude, current_velocity)
    
    if self._i % 12 == 0: # stupid debugging
      print(f"alt: {current_altitude:.2f}m,\tvol: {vol:.2f}m3,\
\tbuoy: {buoy:.2f}N,\
\tdrag: {drag:.2f}N,\
\trho: {rho:.4f}kg/m3,\
\tweight: {weight:.2f}N,\
\tmass: {mass:.1f}kg,\
\tvel: {current_velocity:.2f}m/s,\
\tacc: {acc:.4f}m/s2")
    self._i += 1

    return delta

