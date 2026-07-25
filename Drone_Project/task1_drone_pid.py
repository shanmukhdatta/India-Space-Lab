"""
Task 1: Understanding PID Controller Design Using Drone Altitude Control
-------------------------------------------------------------------------
The drone attempts to reach and hold a desired altitude using a PID
controller. A wind disturbance is switched on after t = 6 s so that the
effect of the disturbance on stability / tracking can be observed.

This script can be run two ways:
1. As a plain script:
       python task1_drone_pid.py
   It will save 'pid_tuning_result.png' in the current folder using the
   final tuned gains (Kp=6.0, Kd=4.0, Ki=0.5).
2. Inside Jupyter/Colab (as in the project notebook): running this cell
   also renders interactive sliders for Kp, Kd, Ki, and the wind
   disturbance magnitude, plus a "Run Simulation and Plot" button that
   re-runs the simulation and redraws the plot live.
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
# PID gains  (tuned by hand: P first, then D, then I) -- these are
# the final values used for the slider defaults and for the static
# plot produced when this file is run directly.
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


def plot_result(altitude_history, Kp, Ki, Kd, save=True, filename="pid_tuning_result.png"):
    """Draw the altitude-vs-time plot for a given simulation result."""
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
    if save:
        plt.savefig(filename, dpi=150)
        print(f"Saved {filename}")
    plt.show()

    overshoot = max(altitude_history) - target_altitude
    print(f"Max overshoot: {overshoot:.3f} m")


if __name__ == "__main__":
    altitude_history, error_history = simulate(Kp, Ki, Kd, wind_disturbance)
    plot_result(altitude_history, Kp, Ki, Kd, save=True, filename="pid_tuning_result.png")


# ---------------------------------------------------------------
# Interactive sliders + "Run Simulation and Plot" button
# ---------------------------------------------------------------
# Only builds the interactive UI when this code is executed inside a
# Jupyter / Colab notebook (so plain `python task1_drone_pid.py` from a
# terminal keeps behaving exactly as before, producing the static PNG).
def _in_notebook():
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell is not None and shell.__class__.__name__ in (
            "ZMQInteractiveShell",  # Jupyter / Colab
            "Shell",                # some Colab kernels
        )
    except Exception:
        return False


def build_interactive_ui():
    """Build sliders for Kp, Kd, Ki, wind disturbance and a run button
    that re-simulates and redraws the altitude-hold plot live."""
    import ipywidgets as widgets
    from IPython.display import display, clear_output

    kp_slider = widgets.FloatSlider(value=Kp, min=0.0, max=15.0, step=0.1, description="Kp:")
    kd_slider = widgets.FloatSlider(value=Kd, min=0.0, max=10.0, step=0.1, description="Kd:")
    ki_slider = widgets.FloatSlider(value=Ki, min=0.0, max=3.0, step=0.05, description="Ki:")
    wind_slider = widgets.FloatSlider(value=wind_disturbance, min=0.0, max=8.0, step=0.1, description="Wind:")

    run_button = widgets.Button(description="Run Simulation and Plot", button_style="success")
    output = widgets.Output()

    def on_run_clicked(_):
        with output:
            clear_output(wait=True)
            alt_hist, _ = simulate(kp_slider.value, ki_slider.value, kd_slider.value, wind_slider.value)
            # Only overwrite the official PNG when the sliders match the
            # final tuned values, so the submitted plot stays valid.
            is_final_tuning = (
                kp_slider.value == Kp and kd_slider.value == Kd
                and ki_slider.value == Ki and wind_slider.value == wind_disturbance
            )
            plot_result(alt_hist, kp_slider.value, ki_slider.value, kd_slider.value,
                        save=is_final_tuning, filename="pid_tuning_result.png")

    run_button.on_click(on_run_clicked)

    ui = widgets.VBox([kp_slider, kd_slider, ki_slider, wind_slider, run_button, output])
    display(ui)
    # Show the final tuned result once on first display.
    on_run_clicked(None)


if _in_notebook():
    build_interactive_ui()
