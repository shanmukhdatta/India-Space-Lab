"""
Task 2: Understanding Guidance and Path Tracking Using an Autonomous Boat
--------------------------------------------------------------------------
The boat tries to follow a predefined trajectory (blue dotted line) using a
simple Line-Of-Sight (LOS) guidance law with a P+D heading controller.
Water current is modelled as a constant disturbance (current_x, current_y)
added directly to the boat's velocity.

Run this file directly:
    python task2_boat_guidance.py
It will save two plots:
    boat_guidance_with_current.png
    boat_guidance_without_current.png
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Desired path (a gentle curve) - this is the "blue dotted line"
# ---------------------------------------------------------------
path_t = np.linspace(0, 40, 800)
path_x = path_t
path_y = 4.0 * np.sin(0.25 * path_t)

# ---------------------------------------------------------------
# Controller gains (tuned using the slider-style search suggested
# in the assignment: kp first, then kd)
# ---------------------------------------------------------------
kp = 1.8
kd = 0.6

dt = 0.05
sim_time = 42.0
speed = 1.2          # constant forward speed of the boat (m/s)
lookahead = 6         # index-based lookahead along the path array


def wrap_angle(angle):
    """Wrap an angle to the range [-pi, pi]."""
    return (angle + np.pi) % (2 * np.pi) - np.pi


def simulate_boat(current_x, current_y):
    x, y, theta = 0.0, 0.0, 0.0
    prev_heading_error = 0.0

    xs, ys = [x], [y]
    steps = int(sim_time / dt)

    for i in range(steps):
        # find nearest path point ahead of the boat, then look ahead further
        dists = (path_x - x) ** 2 + (path_y - y) ** 2
        nearest_idx = np.argmin(dists)
        target_idx = min(nearest_idx + lookahead, len(path_x) - 1)

        target_x = path_x[target_idx]
        target_y = path_y[target_idx]

        desired_heading = np.arctan2(target_y - y, target_x - x)
        heading_error = wrap_angle(desired_heading - theta)

        d_error = (heading_error - prev_heading_error) / dt
        prev_heading_error = heading_error

        omega = kp * heading_error + kd * d_error
        theta += omega * dt

        # boat kinematics, current acts as an additive drift
        x += (speed * np.cos(theta) + current_x) * dt
        y += (speed * np.sin(theta) + current_y) * dt

        xs.append(x)
        ys.append(y)

        if nearest_idx >= len(path_x) - 2:
            break

    return np.array(xs), np.array(ys)


def plot_result(xs, ys, current_x, current_y, filename, title):
    plt.figure(figsize=(9, 5))
    plt.plot(path_x, path_y, "b--", label="Desired Path", linewidth=1.5)
    plt.plot(xs, ys, color="tab:orange", label="Boat Trajectory", linewidth=1.8)
    plt.scatter([xs[0]], [ys[0]], color="green", zorder=5, label="Start")
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"Saved {filename}")


if __name__ == "__main__":
    # Case 1: WITH disturbance / current
    current_x, current_y = 0.3, 0.2
    xs, ys = simulate_boat(current_x, current_y)
    plot_result(
        xs, ys, current_x, current_y,
        "boat_guidance_with_current.png",
        f"Boat Guidance WITH Current (kp={kp}, kd={kd}, current=({current_x},{current_y}))",
    )
    tracking_error = np.mean(np.sqrt((np.interp(xs, path_x, path_y) - ys) ** 2))
    print(f"With current -> mean tracking deviation approx: {tracking_error:.3f} m")

    # Case 2: WITHOUT disturbance / current (ideal conditions, as required)
    current_x, current_y = 0, 0
    xs, ys = simulate_boat(current_x, current_y)
    plot_result(
        xs, ys, current_x, current_y,
        "boat_guidance_without_current.png",
        f"Boat Guidance WITHOUT Current (kp={kp}, kd={kd}, current=(0,0))",
    )
    tracking_error = np.mean(np.sqrt((np.interp(xs, path_x, path_y) - ys) ** 2))
    print(f"Without current -> mean tracking deviation approx: {tracking_error:.3f} m")
