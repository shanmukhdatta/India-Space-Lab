# Advanced Drone Technology Project — Detailed Project Report

**Student:** Boda Shanmukha Datta  
**ISL Enrolment No.:** ISL-177115  
**Institution:** NIT Jalandhar  
**Email:** bodasd.ic.24@nitj.ac.in  

---

## 1. What Is This Project?

This project teaches the fundamentals of **autonomous vehicle control** using Python simulations. Instead of flying a real drone, we use mathematical models to simulate:

1. A **drone** trying to hold a fixed altitude (using PID control)
2. An **autonomous boat** following a curved path on water (using guidance laws)
3. A **bonus drone** flying a figure-eight pattern (trajectory tracking)

These are the same control principles used in real drones, self-driving cars, rockets, and satellites — but simplified so beginners can understand and experiment.

---

## 2. Theoretical Background (Beginner Explanation)

### 2.1 What Is Control Theory?

**Control theory** answers the question: *"How do I make a machine do what I want?"*

Every autonomous system has:
- **Setpoint (target)** — what we want (e.g., altitude = 10 m)
- **Current state** — where we actually are (e.g., altitude = 7 m)
- **Error** — difference between target and current (e.g., error = 3 m)
- **Controller** — calculates corrective action based on error
- **Actuator** — applies the correction (e.g., increase motor thrust)

```
Target (10m) ──→ [Controller] ──→ [Drone] ──→ Actual altitude
                      ↑                              │
                      └──────── Error ←──────────────┘
```

### 2.2 PID Controller (Task 1)

**PID** stands for **Proportional – Integral – Derivative**. It is the most common controller in engineering.

| Term | Symbol | What It Does | Analogy |
|------|--------|--------------|---------|
| **Proportional** | P (Kp) | Reacts to current error | "I'm 3m below target → push up hard" |
| **Integral** | I (Ki) | Reacts to accumulated past error | "I've been below target for 5 seconds → push up more" |
| **Derivative** | D (Kd) | Reacts to rate of change of error | "I'm approaching target fast → ease off to avoid overshoot" |

**Control equation:**
```
Output = Kp × error + Ki × ∫(error)dt + Kd × d(error)/dt
```

**Tuning order (as taught in assignment):**
1. Start with **P only** — increase Kp until response is fast but oscillates
2. Add **D** — increase Kd to reduce oscillation/overshoot
3. Add **I** — increase Ki to eliminate steady-state error (offset from target)

**Why wind disturbance?**
Real drones face wind. Testing with a disturbance at t = 6 s shows whether the controller can **reject disturbances** and return to the target altitude.

### 2.3 Guidance and Path Tracking (Task 2)

**Guidance** means deciding *where to go*. **Control** means *how to get there*.

For the autonomous boat:
- **Desired path** — a predefined curve the boat must follow
- **Line-of-Sight (LOS) guidance** — the boat looks ahead on the path and steers toward a "lookahead point"
- **Heading controller** — P+D controller adjusts the boat's heading angle

**How LOS works (simple explanation):**
1. Find the nearest point on the desired path
2. Look ahead a few points further along the path
3. Calculate the angle from boat to that lookahead point
4. Steer the boat to match that angle

**Water current** acts as a disturbance — it pushes the boat sideways. The controller must compensate by steering differently.

### 2.4 Trajectory Tracking (Bonus Task)

Instead of holding a fixed position, the drone must follow a **moving target** that traces a figure-eight path.

- **Desired path:** Lemniscate of Gerono (figure-eight shape)
  ```
  x(t) = A × sin(ωt)
  y(t) = A × sin(ωt) × cos(ωt)
  ```
- **PD position controller** — separate controllers for x and y directions
- Each axis computes: `acceleration = Kp × position_error + Kd × velocity_error`

---

## 3. Tasks Given (Assignment Requirements)

| # | Task | Description | File |
|---|------|-------------|------|
| 1 | PID Altitude Control | Drone holds 10 m altitude; wind disturbance at t = 6 s | `task1_drone_pid.py` |
| 2 | Boat Path Tracking | Boat follows curved path with/without water current | `task2_boat_guidance.py` |
| 3 | Bonus: Figure-Eight | Drone tracks a figure-eight trajectory under wind | `bonus_figure_eight_drone.py` |
| 4 | Jupyter Notebook | All tasks combined in interactive notebook | `Advanced_Drone_Technology_Project.ipynb` |

**Deliverables for each task:**
- Working Python simulation code
- Tuned controller gains with explanation
- Plot showing desired vs. actual trajectory
- Performance metrics (overshoot, tracking error)

---

## 4. Task 1 — PID Drone Altitude Control

### 4.1 Problem Statement

A drone starts on the ground and must climb to and hold **10 meters altitude**. After 6 seconds, a **wind disturbance** pushes it downward. The PID controller must recover and maintain altitude.

### 4.2 Physics Model (Simplified)

We model the drone as a point mass with:
```
acceleration = control_output - wind_disturbance
velocity += acceleration × dt
altitude += velocity × dt
```

Gravity is assumed already compensated (the controller output directly represents thrust adjustment).

### 4.3 How I Executed Task 1

**Step 1 — Set up simulation parameters:**
```python
dt = 0.01          # time step: 0.01 seconds (100 updates per second)
t_end = 20.0       # simulate for 20 seconds
target_altitude = 10.0  # goal: 10 meters
wind_start_time = 6.0   # wind starts at 6 seconds
wind_disturbance = 3.0  # wind pushes with 3 m/s² force
```

**Step 2 — Tuned PID gains (P first, then D, then I):**

| Gain | Value | Reason |
|------|-------|--------|
| Kp = 6.0 | Proportional | Strong response to altitude error — climbs quickly |
| Kd = 4.0 | Derivative | Dampens oscillation — prevents overshooting past 10 m |
| Ki = 0.5 | Integral | Eliminates small steady offset after disturbance |

**Step 3 — Ran simulation loop:**
```python
for each time step:
    error = target_altitude - current_altitude
    integral_error += error × dt
    derivative_error = (error - previous_error) / dt
    
    control = Kp×error + Ki×integral_error + Kd×derivative_error
    
    if time >= 6 seconds:
        apply wind disturbance
    
    acceleration = control - wind_force
    update velocity and altitude
```

**Step 4 — Plotted results and saved `pid_tuning_result.png`**

### 4.4 What Happens in the Simulation

| Time Period | What Happens |
|-------------|--------------|
| 0 – ~3 s | Drone climbs rapidly toward 10 m (P term dominates) |
| ~3 – 6 s | Drone settles near 10 m with minimal overshoot (D term dampens) |
| 6 s | Wind disturbance applied — altitude drops |
| 6 – ~10 s | PID controller fights back — altitude recovers to 10 m |
| 10 – 20 s | Stable hold at 10 m (I term eliminates residual offset) |

### 4.5 Results

- **Output file:** `pid_tuning_result.png`
- Drone successfully reaches and holds 10 m altitude
- Recovers from wind disturbance within ~4 seconds
- Minimal overshoot due to Kd damping

---

## 5. Task 2 — Autonomous Boat Guidance

### 5.1 Problem Statement

An autonomous boat must follow a predefined curved path. Test two cases:
1. **With water current** (disturbance)
2. **Without water current** (ideal conditions)

### 5.2 Desired Path

A gentle sinusoidal curve:
```
x = t
y = 4 × sin(0.25 × t)
```

This creates a wavy path from (0, 0) to approximately (40, 0).

### 5.3 How I Executed Task 2

**Step 1 — Defined the path and controller:**
```python
path_x = t                    # x increases linearly
path_y = 4.0 × sin(0.25 × t) # y oscillates

kp = 1.8    # proportional heading gain
kd = 0.6    # derivative heading gain
speed = 1.2  # boat moves at 1.2 m/s
lookahead = 6  # look 6 points ahead on path
```

**Step 2 — Implemented LOS guidance loop:**
```python
for each time step:
    1. Find nearest point on desired path to boat
    2. Look ahead 6 points further along path
    3. Calculate desired heading angle to lookahead point
    4. heading_error = desired_heading - current_heading
    5. omega = kp × heading_error + kd × d(heading_error)/dt
    6. Update boat heading: theta += omega × dt
    7. Move boat: x += (speed × cos(theta) + current_x) × dt
                  y += (speed × sin(theta) + current_y) × dt
```

**Step 3 — Ran two cases:**

| Case | Current (m/s) | Output File |
|------|---------------|-------------|
| With current | (0.3, 0.2) | `boat_guidance_with_current.png` |
| Without current | (0, 0) | `boat_guidance_without_current.png` |

### 5.4 What Happens in the Simulation

**Without current (ideal):**
- Boat closely follows the blue dashed desired path
- Small deviations only at sharp curves
- Best tracking performance

**With current (disturbance):**
- Water pushes boat sideways continuously
- Controller compensates by steering into the current
- Path deviation is larger but boat still follows general route
- Demonstrates robustness of LOS guidance

### 5.5 Results

- **Output files:** `boat_guidance_with_current.png`, `boat_guidance_without_current.png`
- Boat successfully tracks the sinusoidal path in both cases
- Tracking error is higher with current (as expected)
- P+D heading controller provides smooth steering

---

## 6. Bonus Task — Figure-Eight Drone Trajectory

### 6.1 Problem Statement

A drone must follow a **figure-eight (lemniscate)** path while facing constant wind disturbance. This is harder than altitude hold because the target is constantly moving.

### 6.2 Figure-Eight Path (Lemniscate of Gerono)

```
x(t) = A × sin(ωt)
y(t) = A × sin(ωt) × cos(ωt)
```

Where:
- A = 5.0 m (amplitude — size of the figure-eight)
- ω = 0.4 rad/s (speed of traversal)

### 6.3 How I Executed the Bonus Task

**Step 1 — Generated the desired path:**
```python
A = 5.0
omega = 0.4
target_x = A × sin(omega × t)
target_y = A × sin(omega × t) × cos(omega × t)
```

**Step 2 — Implemented PD position controller (separate x and y):**
```python
Kp = 8.0   # position gain
Kd = 5.0   # velocity gain

for each time step:
    error_x = target_x[i] - drone_x
    error_y = target_y[i] - drone_y
    
    accel_x = Kp × error_x + Kd × d(error_x)/dt
    accel_y = Kp × error_y + Kd × d(error_y)/dt
    
    if wind_enabled:
        accel_x += wind_x   # 0.4 m/s²
        accel_y += wind_y   # -0.3 m/s²
    
    update drone velocity and position
```

**Step 3 — Plotted desired path vs. actual drone trajectory**

### 6.4 What Happens in the Simulation

- Drone starts at origin (0, 0)
- Initially lags behind the moving figure-eight target
- PD controller accelerates drone toward the target point
- After ~3–5 seconds, drone closely tracks the figure-eight
- Wind causes slight offset but controller compensates
- Orange line (drone) follows blue dashed line (desired path)

### 6.5 Results

- **Output file:** `figure_eight_drone_tracking.png`
- Drone successfully follows the figure-eight pattern
- Wind disturbance causes minor tracking error but path is maintained
- Demonstrates 2D trajectory tracking capability

---

## 7. Files Created

| File | Purpose | Output Generated |
|------|---------|------------------|
| `task1_drone_pid.py` | PID altitude control simulation | `pid_tuning_result.png` |
| `task2_boat_guidance.py` | LOS boat path tracking | `boat_guidance_with_current.png`, `boat_guidance_without_current.png` |
| `bonus_figure_eight_drone.py` | Figure-eight trajectory tracking | `figure_eight_drone_tracking.png` |
| `Advanced_Drone_Technology_Project.ipynb` | All tasks in Jupyter notebook | Same plots inline |

---

## 8. How to Run

```bash
cd Drone_Project

# Task 1: PID altitude control
python task1_drone_pid.py

# Task 2: Boat guidance (generates 2 plots)
python task2_boat_guidance.py

# Bonus: Figure-eight drone
python bonus_figure_eight_drone.py
```

**Requirements:**
```bash
pip install numpy matplotlib
```

**Optional (for notebook):**
```bash
pip install jupyter
jupyter notebook Advanced_Drone_Technology_Project.ipynb
```

---

## 9. Key Concepts Learned

| Concept | Where Used | Real-World Application |
|---------|------------|------------------------|
| PID Control | Task 1 | Drone altitude hold, cruise control in cars |
| Disturbance Rejection | Task 1 (wind) | Any system facing external forces |
| Line-of-Sight Guidance | Task 2 | Autonomous boats, missile guidance |
| Path Tracking | Task 2 | Self-driving cars, agricultural robots |
| Trajectory Tracking | Bonus | Camera drones, aerobatic flight |
| Controller Tuning | All tasks | Every feedback control system |

---

## 10. Conclusion

This project demonstrates foundational **guidance, navigation, and control (GNC)** principles through Python simulations:

1. **Task 1** showed how a PID controller maintains altitude and rejects wind disturbances
2. **Task 2** showed how LOS guidance steers a boat along a curved path under water current
3. **Bonus** showed how a PD controller tracks a dynamic figure-eight trajectory in 2D

All simulations use simple physics models and hand-tuned gains, making the control concepts accessible to beginners while reflecting real engineering practice used in drones, rockets, and autonomous vehicles.

---

*See also: [`Drone_Project/`](Drone_Project/) for all source files.*
