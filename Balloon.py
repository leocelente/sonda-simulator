import numpy as np
import Air
from Air import g
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
  m_payload: float = .200
  # Balloon Mass
  m_balloon: float = 1.0

  # Balllon Initial Radius
  r_i: float = 1.4 # m
  # Balllon Burst Radius
  r_f: float = 7.86 # m
  # Balllon Drag Coefficient
  drag_coeff = 0.35

  def volume(self, altitude: float) -> float:
    '''
    Calculates (simplified) the balloon's volume in cubic meters at altitude in meters
    '''
    
    # delta_radius: float = ( ((self.r_i - self.r_f)/(Air.P_sl0 - Air.P_sl2)) * (Air.pressure(altitude) - Air.P_sl2) )
    # radius: float = self.r_f + delta_radius
    
    # P V = n R T
    # 
    k: float = Air.pressure(0) * 4/3*np.pi*self.r_i**3/Air.temperature(altitude)
    burst_vol: float = 4/3*np.pi*self.r_f**3

    vol: float = k * Air.temperature(altitude)/Air.pressure(altitude)

    if vol > burst_vol: # in theory this condition means burst
      return 0

    # vol: float = (4/3)*np.pi*( radius )**3
    return vol

  def density(self, altitude: float) -> float:
    '''
    Calculates the balloon's internal gas density in kilogram per cubic meter at altitude in meters
    '''
    # print(f"calculating density at {altitude} given volume {volume(altitude)}")
    external_pressure: float = Air.pressure(altitude)
    external_temperature = Air.temperature(altitude)
    
    gas_mass:float = (4/3) * np.pi * self.r_i**3 * Air.p_he
    vol: float = self.volume(altitude)
    if vol == 0: # detect burst, so remove heilum (?) and use the surrounding air density
        return Air.density(altitude)
    return gas_mass / vol


  def drag(self, altitude: float, velocity: float) -> float:
    '''
    Calculates the drag force at altitude in meters while moving at velocity in meters per second
    '''
    # radius = self.r_i #! Simplification: radius is constant during ascent

    # This is my modification, I'm using the current volume to estimate the radius
    radius = ((3.0/4.0/np.pi) * self.volume(altitude)) ** (1/3)
    area: float = np.pi * radius * radius
    
    # print(f"calculating drag at {altitude} and vel: {velocity} given air_den {air_density(altitude)}")
    return (1/2) * self.drag_coeff * Air.density(altitude) * area * ((velocity)*velocity)

  def mass(self):
    # Expected Helium Mass 
    m_gas: float = self.volume(0) * self.density(0)
    mass: float = self.m_payload + self.m_balloon + m_gas
    return mass

  def weight(self) -> float:
    '''
    Total Weight
    '''
    return self.mass() * g

  def buoyancy(self, altitude: float) -> float:
    '''
    Calculates the Buoyancy force at a given altitude
    '''

    # print(f"calculating buoyancy at {altitude} given volume {volume(altitude)}, air_den {air_density(altitude)} and gas_den {density(altitude)}")
    return g * self.volume(altitude) * (Air.density(altitude) - self.density(altitude)) 


  def acceleration(self, altitude: float, velocity: float) -> float:
    '''
    Calculates the acceleration in meters per second square from altitude and (previous dt) velocity
    '''
    # print(f"calculating acceleration given buoyancy: {buoyancy(altitude)}, Weight: {weight()} and Drag: {drag(altitude, velocity)}")
    return (self.buoyancy(altitude) - self.weight() - self.drag(altitude, velocity)) / self.mass()


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
    
    if current_altitude < 33e3: # stupid debugging
      print(f"alt: {current_altitude:.2f}m,\tvol: {vol:.2f}m3,\tbuoy: {buoy:.2f}N,\tdrag: {drag:.2f}N,\trho: {rho:.2f}kg/c3,\tweight: {weight:.2f}N,\tmass: {mass:.2f}kg,\tvel: {current_velocity:.2f}m/s,\tacc: {acc:.2f}m/s2")

    return delta
