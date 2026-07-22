"""
Task 1: Understanding PID Controller Design Using Drone Altitude Control
-------------------------------------------------------------------------
The drone attempts to reach and hold a desired altitude using a PID
controller. A wind disturbance is switched on after t = 6 s so that the
effect of the disturbance on stability / tracking can be observed.

Run this file directly:
    python task1_drone_pid.py
It will save 'pid_tuning_result.png' in the current folder.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Simulation parameters
# ---------------------------------------------------------------
dt = 0.01                 # time step (s)
t_end = 20.0               # total simulation time (s)
t = np.arange(0, t_end, dt)

mass = 1.0                 # kg  (simplified drone mass)
g = 9.81                   # m/s^2

target_altitude = 10.0     # m, desired altitude

# Wind disturbance settings
wind_start_time = 6.0       # s, "no wind zone" is 0-6 s
wind_disturbance = 3.0      # m/s^2 equivalent extra downward/side force after 6s

# ---------------------------------------------------------------
# PID gains  (tuned by hand: P first, then D, then I)
# ---------------------------------------------------------------
Kp = 6.0
Kd = 4.0
Ki = 0.5


def simulate(Kp, Ki, Kd, wind_mag):
    """Run the altitude-hold simulation and return time history arrays."""
    altitude = 0.0
    velocity = 0.0
    integral_error = 0.0
    prev_error = target_altitude - altitude

    altitude_history = []
    error_history = []

    for time_step in t:
        error = target_altitude - altitude
        integral_error += error * dt
        derivative_error = (error - prev_error) / dt
        prev_error = error

        # PID control output -> commanded thrust acceleration
        control = Kp * error + Ki * integral_error + Kd * derivative_error

        # Total acceleration = thrust (control), with gravity already
        # compensated by the hover baseline, minus the wind disturbance
        wind_force = wind_mag if time_step >= wind_start_time else 0.0
        acceleration = control - wind_force

        velocity += acceleration * dt
        altitude += velocity * dt

        altitude_history.append(altitude)
        error_history.append(error)

    return np.array(altitude_history), np.array(error_history)


if __name__ == "__main__":
    altitude_history, error_history = simulate(Kp, Ki, Kd, wind_disturbance)

    plt.figure(figsize=(9, 5))
    plt.plot(t, altitude_history, label="Drone Altitude", color="tab:blue")
    plt.axhline(target_altitude, color="black", linestyle="--", linewidth=1, label="Target Altitude")
    plt.axvline(wind_start_time, color="red", linestyle=":", linewidth=1.5, label="Wind Disturbance Introduced (t=6s)")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.title(f"PID Controller Tuning Result (Kp={Kp}, Ki={Ki}, Kd={Kd})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("pid_tuning_result.png", dpi=150)
    print("Saved pid_tuning_result.png")

    # Simple performance metrics printed for the report
    overshoot = max(altitude_history) - target_altitude
    settle_band = 0.05 * target_altitude
    print(f"Max overshoot: {overshoot:.3f} m")
