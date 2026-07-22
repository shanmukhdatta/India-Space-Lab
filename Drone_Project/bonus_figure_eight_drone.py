"""
Creative Bonus Task: Drone Figure-Eight Trajectory Tracking
-------------------------------------------------------------
The desired path is a lemniscate (figure-eight) defined by parametric
equations. A simple PD position controller (independently on x and y)
drives the drone to follow the moving target point along the figure
eight, and wind disturbance can optionally be enabled.

Run this file directly:
    python bonus_figure_eight_drone.py
It will save 'figure_eight_drone_tracking.png'.
"""

import numpy as np
import matplotlib.pyplot as plt

dt = 0.01
t_end = 20.0
t = np.arange(0, t_end, dt)

A = 5.0        # amplitude (m)
omega = 0.4    # angular speed of the figure-eight (rad/s)

# Parametric equations of a figure-eight (Lemniscate of Gerono)
target_x = A * np.sin(omega * t)
target_y = A * np.sin(omega * t) * np.cos(omega * t)

# PD controller gains for x and y position loops
Kp = 8.0
Kd = 5.0

wind_enabled = True
wind_x, wind_y = 0.4, -0.3   # constant wind disturbance (m/s^2)


def simulate():
    x, y = 0.0, 0.0
    vx, vy = 0.0, 0.0
    prev_ex, prev_ey = target_x[0] - x, target_y[0] - y

    xs, ys = [], []

    for i, current_t in enumerate(t):
        ex = target_x[i] - x
        ey = target_y[i] - y

        dex = (ex - prev_ex) / dt
        dey = (ey - prev_ey) / dt
        prev_ex, prev_ey = ex, ey

        ax = Kp * ex + Kd * dex
        ay = Kp * ey + Kd * dey

        if wind_enabled:
            ax += wind_x
            ay += wind_y

        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)


if __name__ == "__main__":
    xs, ys = simulate()

    plt.figure(figsize=(7, 7))
    plt.plot(target_x, target_y, "b--", label="Desired Figure-Eight Path", linewidth=1.5)
    plt.plot(xs, ys, color="tab:orange", label="Drone Trajectory", linewidth=1.8)
    plt.scatter([0], [0], color="green", zorder=5, label="Start")
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.title("Bonus Task: Drone Following a Figure-Eight Trajectory")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("figure_eight_drone_tracking.png", dpi=150)
    print("Saved figure_eight_drone_tracking.png")
