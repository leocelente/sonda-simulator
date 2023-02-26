"""Balloon Numerical Model."""
import numpy as np
import Air
from Universe import radius_sphere, vol_sphere, molar_mass_he, g, R
from Instrument import probe
from numpy import ndarray
from datetime import datetime, timedelta
from thirdparty.GFS import GFS_Handler
from thirdparty.global_tools import dirspeed2uv, m2deg
from typing import Callable

# ? Mass:           Kilogram
# ? Preassure:      Pascal
# ? Temperature:    Kelvin
# ? Altitude:       meter
# ? Force:          Newton
# ? Time:           seconds
# ? Density:        Kg/m^3
# ? Volume:         m^3
# ? Acceleration:   m/s^2


class Balloon():
    """Contains the numeric models to simulate the balloon ascent."""

    # Payload Mass
    m_payload: float
    # Balloon Mass
    m_balloon: float

    # Initial Gas Volume
    vol_gas_i: float

    # Balllon Initial Radius
    r_i: float
    # Balllon Burst Radius
    r_f: float
    # Balllon Drag Coefficient
    drag_coeff: float
    # Helps check if this iteration is a burst
    burst: bool
    # Check if it hit the ground
    touchdown: bool

    # Parachute Drag Coefficient
    parachute_Dcoeff: float
    # Parachute Radius
    parachute_r: float
    initial_m_gas: float
    initial_loc: tuple[float, float]
    start_date: datetime
    # All are generated with signature: (latitude, longitude, altitude, gfs_time) -> float
    forecast_pressure = Callable[[float, float, float, float], float]
    forecast_temperature = Callable[[float, float, float, float], float]
    forecast_wind_dir = Callable[[float, float, float, float], float]
    forecast_wind_spd = Callable[[float, float, float, float], float]
    gfs_link: GFS_Handler

    def __init__(self, balloon_mass: float, payload_mass: float, initial_volume: float, burst_diameter: float, drag_coef: float, parachute_diameter: float, initial_loc: tuple[float, float], start_date: datetime, parachute_drag_coeff: float) -> None:
        """
        Create balloon object.

        balloon_mass: 1000g, 2000g etc
        payload_mass: in kilograms
        initial_volume: balloon filled volume (m3)
        burst_diameter: ballon burst diameter (m)
        drag_coef: Drag Coefficient
        parachute_diameter:
        parachute_drag_coeff:
        """
        self.m_balloon = balloon_mass * 1e-3
        self.m_payload = payload_mass
        self.vol_gas = initial_volume
        self.r_i = radius_sphere(initial_volume)
        self.r_f = burst_diameter / 2
        self.drag_coeff = drag_coef
        self.parachute_Dcoeff = parachute_drag_coeff
        self.parachute_r = parachute_diameter / 2
        self.initial_m_gas = self.vol_gas * Air.p_he
        self.touchdown = False
        self.burst = False
        self.start_date = start_date
        self.initial_loc = initial_loc

        print(f"Payload Mass: {self.m_payload}kg")
        print(f"Balloon:\n \tSize: {balloon_mass}g \n\
      \tInitial Diameter: {initial_volume:.2f}m\n\
      \tInitial Volume: {self.vol_gas:.2f}m3\n\
      \tBurst Diameter: {burst_diameter:.2f}m\n\
      \tExpected He Mass:  {self.initial_m_gas:.4f}kg\n\
      \tDrag Coefficient: {drag_coef:.3f}")

        print(
            f"Parachute: \n \tOpen Diameter: {parachute_diameter:.2f}m\n \tDrag Coefficient: {parachute_drag_coeff:.3f}")

        self.gfs_link = GFS_Handler(
            self.initial_loc[0], self.initial_loc[1], self.start_date)
        print(f"Downloading Forecast data from NASA's GFS...")
        self.gfs_link.downloadForecast()
        print(f"Complete")
        getTemp, getPress = self.gfs_link.interpolateData('temperature', 'pressure')
        getDir, getSpd = self.gfs_link.interpolateData('wind_direction', 'wind_speed')
        self.forecast_temperature = getTemp
        self.forecast_pressure = getPress
        self.forecast_wind_dir = getDir
        self.forecast_wind_spd = getSpd

    def volume(self, altitude: float, m_gas: float) -> float:
        """Calculate (simplified) the balloon's volume in cubic meters at altitude in meters."""
        if (self.burst):
            return 0

        burst_vol: float = vol_sphere(self.r_f)

        # Ideal Gas Law
        # initial gas mass
        # m_0: float  = vol_sphere(self.r_i) * Air.p_he
        # m_gas = m_0                                     #! Assumption

        pressure: float = Air.pressure(altitude)          # ! Assumption
        # pressure =    4/3 * np.pi * g * self.density(altitude, m_gas) * altitude
        temperature: float = Air.temperature(altitude)    # ! Assumption
        vol: float = m_gas * R * temperature / pressure / molar_mass_he

        # radius = self.r_f + (self.r_i - self.r_f)/(Air.P_sl0 -
        #                                            Air.P_sl2)*(Air.pressure(altitude) - Air.P_sl2)
        # vol = vol_sphere(radius)

        if vol > burst_vol:  # in theory this condition means burst
            self.burst = True

        return vol

    def drag(self, altitude: float, velocity: float, m_gas: float) -> float:
        """Calculate the drag force at altitude in meters while moving at velocity in meters per second."""
        if (self.burst):
            self.drag_coeff = self.parachute_Dcoeff
            area = np.pi * (self.parachute_r) ** 2
        else:
            radius = radius_sphere(self.volume(altitude, m_gas))
            area: float = np.pi * radius * radius

        d: float = -(1/2) * self.drag_coeff * \
            Air.density(altitude) * area * (abs(velocity)*velocity)
        return d

    def mass(self, m_gas: float) -> float:
        """Calculate current system mass."""
        # Expected Helium Mass
        # m_gas: float = vol_sphere(self.r_i) * Air.p_he

        if (self.burst):
            self.m_balloon = 0
            self.m_gas = 0

        mass: float = self.m_payload + self.m_balloon + m_gas
        return mass

    def weight(self, m_gas: float) -> float:
        """Total Weight."""
        # m_gas: float = vol_sphere(self.r_i) * Air.p_he
        return -(self.mass(m_gas)) * g

    def density(self, altitude: float, m_gas: float) -> float:
        """Calculate current gas density inside balloon (He)."""
        if (self.burst):
            return 0

        # m_gas: float =  vol_sphere(self.r_i) * Air.p_he
        rho_he = m_gas / self.volume(altitude, m_gas)
        return rho_he

    def buoyancy(self, altitude: float, m_gas: float) -> float:
        """Calculate the Buoyancy force at a given altitude."""
        return g * self.volume(altitude, m_gas) * (Air.density(altitude) - self.density(altitude, m_gas))

    def acceleration(self, altitude: float, velocity: float, m_gas: float) -> float:
        """Calculate acceleration in m/s2 from altitude and (previous dt) velocity."""
        acc: float = (self.buoyancy(altitude, m_gas) + self.weight(m_gas) +
                      self.drag(altitude, velocity, m_gas)) / self.mass(m_gas)
        self.r_i += 0.1
        if (self.touchdown):
            # ! Assumption: Contact time of 0.5s
            acc = (0 - velocity)/(0.5 - 0)
        return acc

    last_error = 0
    acc_error = 0

    def valve(self, altitude: float, current_m_gas: float, velocity: float) -> float:
        """Gas Mass change by valve"""
        r = 0.01
        area = np.pi * r * r
        # vazao = area * (np.sqrt(2 * (self.pressure() - Air.pressure(altitude))))

        vazao = 0

        P = 0.1
        I = 0.0
        D = 0.01

        setpoint = 0
        error = velocity - setpoint
        if (altitude > 19e3 and False):
            vazao = P * error + I * (self.acc_error) + \
                D * (error - self.last_error)

        self.last_error = error
        self.acc_error += error

        self.acc_error = self.acc_error if self.acc_error < 10 else 0

        return -vazao * self.density(altitude, current_m_gas)

    _i = 0

    def delta_loc(self, lat, lng, alt, velocity: float, time) -> float:
        # direction in [degrees] clockwise from north
        dir_deg = self.forecast_wind_dir(lat, lng, alt, self.gfs_link.getGFStime(
            self.start_date+timedelta(seconds=time)))
        # speed in [knots]
        spd_knots = self.forecast_wind_spd(lat, lng, alt, self.gfs_link.getGFStime(
            self.start_date+timedelta(seconds=time)))
        spd = spd_knots * 0.514444 # m/s
        u,v = dirspeed2uv(dir_deg, spd)
        return m2deg(u, v, lat)

    def Model(self, t: float, state: list[list[float]]) -> ndarray:
        """Calculate the derivative (delta state) to be integrated on simulation step."""
        current_altitude: float = state[0][0]          # altitude
        current_velocity: float = state[1][0]          # velocity
        current_m_gas: float = state[2][0]
        current_lat: float = state[3][0]
        current_lng: float = state[4][0]

        if self.burst and current_altitude < 1e-3:
            self.touchdown = True

        delta = np.vstack([current_velocity,  # altitude
                           self.acceleration(
                               current_altitude, current_velocity, current_m_gas),  # velocity
                           self.valve(current_altitude,
                                      current_m_gas, current_velocity), # volume
                           *self.delta_loc(current_lat, current_lng,
                                          current_altitude, current_velocity, t) # lat, lng
                           ])

        probe(self.volume(current_altitude, current_m_gas), 0)
        probe(self.buoyancy(current_altitude, current_m_gas), 1)
        probe(self.drag(current_altitude, current_velocity, current_m_gas), 2)
        probe(self.acceleration(current_altitude,
                                current_velocity, current_m_gas), 3)
        probe(self.weight(current_m_gas), 4)
        probe(Air.temperature(current_altitude), 5)
        probe(Air.pressure(current_altitude), 6)
        probe(Air.density(current_altitude), 7)

        self._i += 1
        return delta
