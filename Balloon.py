from cmath import isinf, isnan
import numpy as np
import Air
from Universe import vol_sphere, molar_mass_he, g, R
from Instrument import probe
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
  m_payload: float = 3.3
  # Balloon Mass
  m_balloon: float = 2000e-3

  # Balllon Initial Radius
  r_i: float = 1.4 / 2 # m
  # Balllon Burst Radius
  r_f: float = 8.0 / 2 # m
  # Balllon Drag Coefficient
  drag_coeff: float = 0.35
  # Helps check if this iteration is a burst
  burst: int = 0 

  # Parachute Drag Coefficient
  parachute_Dcoeff: float = 0.65
  # Parachute Radius
  parachute_r: float = 1.3


  def __init__(self, balloon_mass: float, payload_mass: float, initial_diameter: float, burst_diameter: float, drag_coef: float, parachute_diameter: float, parachute_drag_coeff: float) -> None:
    '''
    Creates balloon object
    balloon_mass: 1000g, 2000g etc
    payload_mass: in kilograms
    initial_diameter: balloon start diameter
    burst_diameter: 
    drag_coef: Drag Coefficient
    parachute_diameter:
    parachute_drag_coeff:
    '''
    self.m_balloon = balloon_mass * 1e-3
    self.m_payload = payload_mass
    self.r_i = initial_diameter /2
    self.r_f = burst_diameter /2
    self.drag_coeff = drag_coef
    self.parachute_Dcoeff = parachute_drag_coeff
    self.parachute_r = parachute_diameter /2
    he_mass = vol_sphere(self.r_i) * self.density(altitude=0)
    print(f"Balloon:\n \tSize: {balloon_mass}g \n\
      \tInitial Diameter: {initial_diameter:.2f}m\n\
      \tBurst Diameter: {burst_diameter:.2f}m\n\
      \tExpected He Mass:  {he_mass:.4f}kg/m3\n\
      \tDrag Coefficient: {drag_coef:.3f}")

    print(f"Parachute: \n \tOpen Diameter: {parachute_diameter:.2f}m\n \tDrag Coefficient: {parachute_drag_coeff:.3f}")
    



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
    if(self.burst >= 4): # Helium density doesn't make sense without balloon
      return 0

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
      area = np.pi * (1.5/2)**2
    else: 
      radius = ((3.0/4.0/np.pi) * self.volume(altitude)) ** (1/3)
      area: float = np.pi * radius * radius
    d: float = -(1/2) * self.drag_coeff * Air.density(altitude) * area * (abs(velocity)*velocity)
    return d


  def mass(self) -> float:
    # Expected Helium Mass 
    m_gas: float =  vol_sphere(self.r_i) * self.density(0)

    if(self.burst >= 4):
        self.m_balloon = 0
        m_gas = 0
    mass: float = self.m_payload + self.m_balloon +  m_gas
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
    return g * self.volume(altitude) * Air.density(altitude)


  def acceleration(self, altitude: float, velocity: float) -> float:
    '''
    Calculates the acceleration in meters per second square from altitude and (previous dt) velocity
    '''
     
    acc: float = (self.buoyancy(altitude) + self.weight() + self.drag(altitude, velocity)) / self.mass()
    return acc


  _i = 0
  def Model(self, t: float, state: list[list[float]]) -> list[list[float]]:
    '''
    Calculates the derivative (delta state) to be integrated on simulation step
    '''
    current_altitude: float  = state[0][0]          # altitude
    current_velocity: float  = state[1][0]          # velocity

    delta  = np.vstack([ current_velocity, # altitude
                        self.acceleration(current_altitude, current_velocity) # velocity
    ])

    probe(self.volume(current_altitude), 0)
    probe(self.buoyancy(current_altitude), 1)
    probe(self.drag(current_altitude, current_velocity), 2)
    probe(self.density(current_altitude), 3)
    probe(self.acceleration(current_altitude, current_velocity), 4)
    probe(self.weight(), 5)

      
    self._i += 1
    return delta

