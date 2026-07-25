"""
Task 2: Understanding Guidance and Path Tracking Using an Autonomous Boat
--------------------------------------------------------------------------
The boat tries to follow a predefined trajectory (blue dotted line) using a
simple Line-Of-Sight (LOS) guidance law with a P+D heading controller.
Water current is modelled as a constant disturbance (current_x, current_y)
added directly to the boat's velocity.

This script can be run two ways:
1. As a plain script:
       python task2_boat_guidance.py
   It will save two plots using the final tuned gains (kp=1.8, kd=0.6):
       boat_guidance_with_current.png
       boat_guidance_without_current.png
2. Inside Jupyter/Colab (as in the project notebook): running this cell
   also renders interactive sliders for kp, kd, current_x, current_y, plus
   a "Run Simulation and Plot" button that redraws the path-vs-trajectory
   plot live.
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
# in the assignment: kp first, then kd) -- final tuned values, also
# used as the slider defaults.
# ---------------------------------------------------------------
kp = 1.8
kd = 0.6

dt = 0.05
sim_time = 42.0
speed = 1.2          # constant forward speed of the boat (m/s)
lookahead = 6         # index-based lookahead along the path array

# Final tuned current cases (used for the static plots / PNGs)
current_with = (0.3, 0.2)
current_without = (0.0, 0.0)


def wrap_angle(angle):
    """Wrap an angle to the range [-pi, pi]."""
    return (angle + np.pi) % (2 * np.pi) - np.pi


def simulate_boat(current_x, current_y, kp=kp, kd=kd):
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


def plot_result(xs, ys, current_x, current_y, kp, kd, save=True, filename=None, title=None):
    if title is None:
        title = f"Boat Guidance (kp={kp}, kd={kd}, current=({current_x},{current_y}))"
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
    if save and filename:
        plt.savefig(filename, dpi=150)
        print(f"Saved {filename}")
    plt.show()

    tracking_error = np.mean(np.sqrt((np.interp(xs, path_x, path_y) - ys) ** 2))
    print(f"Mean tracking deviation approx: {tracking_error:.3f} m")


if __name__ == "__main__":
    # Case 1: WITH disturbance / current
    current_x, current_y = current_with
    xs, ys = simulate_boat(current_x, current_y)
    plot_result(
        xs, ys, current_x, current_y, kp, kd, save=True,
        filename="boat_guidance_with_current.png",
        title=f"Boat Guidance WITH Current (kp={kp}, kd={kd}, current=({current_x},{current_y}))",
    )

    # Case 2: WITHOUT disturbance / current (ideal conditions, as required)
    current_x, current_y = current_without
    xs, ys = simulate_boat(current_x, current_y)
    plot_result(
        xs, ys, current_x, current_y, kp, kd, save=True,
        filename="boat_guidance_without_current.png",
        title=f"Boat Guidance WITHOUT Current (kp={kp}, kd={kd}, current=(0,0))",
    )


# ---------------------------------------------------------------
# Interactive sliders + "Run Simulation and Plot" button
# ---------------------------------------------------------------
def _in_notebook():
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell is not None and shell.__class__.__name__ in (
            "ZMQInteractiveShell",
            "Shell",
        )
    except Exception:
        return False


def build_interactive_ui():
    """Build sliders for kp, kd, current_x, current_y and a run button
    that re-simulates and redraws the path-vs-trajectory plot live."""
    import ipywidgets as widgets
    from IPython.display import display, clear_output

    kp_slider = widgets.FloatSlider(value=kp, min=0.0, max=5.0, step=0.1, description="kp:")
    kd_slider = widgets.FloatSlider(value=kd, min=0.0, max=3.0, step=0.05, description="kd:")
    cx_slider = widgets.FloatSlider(value=current_with[0], min=-1.0, max=1.0, step=0.05, description="current_x:")
    cy_slider = widgets.FloatSlider(value=current_with[1], min=-1.0, max=1.0, step=0.05, description="current_y:")

    run_button = widgets.Button(description="Run Simulation and Plot", button_style="success")
    output = widgets.Output()

    def on_run_clicked(_):
        with output:
            clear_output(wait=True)
            xs, ys = simulate_boat(cx_slider.value, cy_slider.value, kp_slider.value, kd_slider.value)
            is_final_with = (kp_slider.value == kp and kd_slider.value == kd
                              and (cx_slider.value, cy_slider.value) == current_with)
            is_final_without = (kp_slider.value == kp and kd_slider.value == kd
                                 and (cx_slider.value, cy_slider.value) == current_without)
            filename = ("boat_guidance_with_current.png" if is_final_with else
                         "boat_guidance_without_current.png" if is_final_without else None)
            plot_result(xs, ys, cx_slider.value, cy_slider.value, kp_slider.value, kd_slider.value,
                        save=filename is not None, filename=filename)

    run_button.on_click(on_run_clicked)

    ui = widgets.VBox([kp_slider, kd_slider, cx_slider, cy_slider, run_button, output])
    display(ui)
    on_run_clicked(None)


if _in_notebook():
    build_interactive_ui()
