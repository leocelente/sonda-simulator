from matplotlib import pyplot as plt
import numpy as np
from Utils import celcius


def Viz(data, time) -> None:
    altitudes = data[:, 0] * 1e-3
    speed = data[:, 1]
    volume = data[:, 2]
    volumes = data[:, 3]
    buoyancy = data[:, 4]
    drag = data[:, 5]
    acceleration = data[:, 6]
    weights = data[:, 7]
    temperature = data[:, 8]
    pressure = data[:, 9]
    density = data[:, 10]
    time_step = time[1] - time[0]
    minutes = time / 60

    def find_burst(x: list[float], y: list[float]):
        i = 1
        current = y[i]
        previous = y[i-1]
        while(current > previous):
            current = y[i]
            previous = y[i-1]
            i += 1
        return (x[i], y[i], i)

    burst_time, burst_altitude, i = find_burst(minutes, altitudes)
    print(f"Burst: {burst_time:.2f}min, {burst_altitude:.2f}km")

    fig = plt.figure(figsize=(14, 8))
    fig.suptitle('Simulation Results', fontsize=16)

    ax = plt.subplot(3, 3, 1)
    if burst_time > minutes[1]:
        print(f"Calculating Linear Aproximation...")
        coefs = np.polyfit(minutes[:i//2], altitudes[:i//2], 1)
        line = np.poly1d(coefs)
        linear_burst_time = (burst_altitude - coefs[1]) / coefs[0]
        print(
            f"Linear Approx. Burst: {linear_burst_time:.2f}min, {line(linear_burst_time):.2f}km")
        i = int(linear_burst_time / time_step * 60)
        plt.plot(minutes, altitudes, linewidth=2,
                 color="black", label='Altitude ($h$)')
        plt.plot(minutes[:i], line(minutes[:i]), color='red')
        plt.ylabel("Altitude (km)")
        plt.grid()

    plt.subplot(3, 3, 2, sharex=ax)
    plt.plot(minutes, volume, linewidth=2,
             color="blue", label="Gas Mass ($h$)")
    plt.ylabel("Volume ($m^3$)")
    plt.grid()

    plt.subplot(3, 3, 3, sharex=ax)
    plt.plot(minutes, speed, linewidth=2, color="orange",
             label="Ascent Rate ($\dot h$)")
    plt.ylabel("Speed (m/s)")
    plt.grid()

    plt.subplot(3, 3, 5, sharex=ax)
    plt.plot(minutes, buoyancy, linewidth=2,
             color="red", label="Buoyancy ($B$)")
    plt.plot(minutes, drag, linewidth=2, color="green", label="Drag ($D$)")
    plt.plot(minutes, weights, linewidth=2,
             color="yellow", label="Weight ($W$)")
    plt.ylabel("Force (N)")
    plt.grid()

    plt.subplot(3, 3, 4, sharex=ax)
    plt.plot(minutes, acceleration, linewidth=2,
             color="purple", label="Acc. ($\ddot h$)")
    plt.ylabel("Acceleration ($m/s^2$)")
    plt.grid()

    ax2 = plt.subplot(3, 3, 6, sharex=ax)
    plt.plot(minutes, volumes, linewidth=2,
             color="blue", label="Volume ($V_{B}$)")
    plt.ylabel("Volume ($m^3$)")
    plt.grid()

    plt.subplot(3, 3, 7, sharex=ax)
    plt.plot(minutes, celcius(temperature))
    plt.legend(["Temperature"])
    plt.ylabel("Temperature (°C)")
    plt.xlabel("Time (minutes)")
    plt.grid()

    plt.subplot(3, 3, 8, sharex=ax)
    plt.plot(minutes, density)
    plt.legend(["Density"])
    plt.ylabel("Density ($kg/m^3$)")
    plt.xlabel("Time (minutes)")
    plt.grid()

    plt.subplot(3, 3, 9, sharex=ax)
    plt.plot(minutes, pressure*1e-2)
    plt.legend(["Pressure"])
    plt.xlabel("Time (min)")
    plt.ylabel("Pressure (kPa)")
    plt.grid()

    plt.show()
