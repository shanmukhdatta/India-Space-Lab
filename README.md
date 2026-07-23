# India Space Lab — Project Portfolio

**Student:** Boda Shanmukha Datta  
**ISL Enrolment No.:** ISL-177115  
**Institution:** NIT Jalandhar  
**Email:** bodasd.ic.24@nitj.ac.in  

This repository contains three independent projects completed as part of the **India Space Lab (ISL)** program. Together they cover satellite ground control software, drone guidance and control simulations, and rocket fin structural/aerodynamic analysis.

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Detailed Project Reports (Beginner-Friendly)](#detailed-project-reports-beginner-friendly)
3. [Project 1 — CanSat Ground Control Software (GCS)](#project-1--cansat-ground-control-software-gcs)
4. [Project 2 — Advanced Drone Technology (Guidance & Control)](#project-2--advanced-drone-technology-guidance--control)
5. [Project 3 — Rocketry FEM & CFD Analysis](#project-3--rocketry-fem--cfd-analysis)
6. [Results Summary](#results-summary)
7. [How to Run All Projects](#how-to-run-all-projects)
8. [Dependencies](#dependencies)
9. [Overall Summary](#overall-summary)

---

## Detailed Project Reports (Beginner-Friendly)

Each project has a separate detailed markdown file with theoretical explanations, task descriptions, step-by-step execution, and results — written for beginners:

| Project | Detailed Report |
|---------|-----------------|
| CanSat GCS | [`CanSat_GCS_Project.md`](CanSat_GCS_Project.md) |
| Drone Technology | [`Drone_Project.md`](Drone_Project.md) |
| Rocketry FEM/CFD | [`Rocketry_Project.md`](Rocketry_Project.md) |

---

## Repository Overview

```
India-Space-Lab-main/
├── cansat_gcs_Project/          # CanSat / CubeSat Ground Control Software (Web app)
├── Drone_Project/               # PID control, boat guidance, figure-eight bonus
├── Rocketry_Project/            # FEM beam analysis, CFD panel method, design optimization
└── README.md                    # This file
```

| Project | Domain | Language / Stack | Key Deliverables |
|---------|--------|------------------|------------------|
| `cansat_gcs_Project` | CanSat / CubeSat mission operations | HTML, CSS, JavaScript (Chart.js, Leaflet, Three.js) | Live telemetry dashboard, serial link, map, 3D orientation, mission control |
| `Drone_Project` | Autonomous guidance & control | Python (NumPy, Matplotlib) | PID altitude hold, boat path tracking, figure-eight trajectory |
| `Rocketry_Project` | Rocket fin structural & aerodynamic analysis | Python (NumPy, Matplotlib) | FEM stress/deflection, CFD pressure field, design optimization |

**Total files:** 30 source and data files across the three project folders.

---

## Project 1 — CanSat Ground Control Software (GCS)

### Description

A single-page **CanSat Ground Control Software** dashboard built for real-time mission monitoring. It receives CSV telemetry packets over USB serial (Web Serial API), parses and displays flight data, tracks GPS position on a map, renders a 3D attitude model, plots live graphs, manages error codes, streams video, and sends mission-critical commands.

### Folder Structure

```
cansat_gcs_Project/
├── index.html                   # Main single-page application
├── css/style.css                # Aerospace HUD theme styling
├── js/
│   ├── app.js                   # App bootstrap, clocks, top-bar wiring
│   ├── telemetry.js             # Packet parsing + telemetry store
│   ├── errorcodes.js            # 4-digit error code logic
│   ├── charts.js                # Real-time Chart.js graphs
│   ├── map.js                   # Leaflet.js GPS tracking map
│   ├── orientation.js           # Three.js 3D orientation model
│   ├── video.js                 # Live video streaming (MediaDevices API)
│   ├── serial.js                # Web Serial link + demo telemetry simulator
│   ├── datamanager.js           # CSV/graph export, packet reset, logging
│   └── missioncontrol.js        # Mission-critical command panel
├── assets/vendor/               # Bundled Chart.js, Leaflet.js, Three.js (offline-capable)
├── arduino/dummy_telemetry.ino  # WeGyanik Kit test sketch (9600 baud)
├── samples/                     # Sample telemetry CSV exports
└── docs/README.md               # Detailed project documentation
```

### Dashboard Panels

| Panel | Function |
|-------|----------|
| Telemetry (Container) | Packet count, mission time, altitude, pressure, temperature, battery, descent rate, GPS satellites |
| Telemetry (Payload) | Roll, pitch, yaw, GPS latitude/longitude/altitude |
| Error Codes | 4-digit fault display (descent, GPS, separation, parachute) |
| Live Graphs | Real-time altitude, pressure, temperature, descent rate charts |
| Tracking Map | Leaflet map with GPS path trail (OpenStreetMap tiles) |
| 3D Orientation | Three.js model showing roll/pitch/yaw |
| Live Video | Camera feed via MediaDevices API |
| Mission Control | Send commands with SENT → ACK logging |

### Telemetry Packet Format

One CSV line per packet, newline-terminated, **9600 baud**:

```
TEAM_ID,PACKET_COUNT,MISSION_TIME,ALTITUDE,PRESSURE,TEMP,VOLTAGE,
DESCENT_RATE,GPS_SATS,GPS_LAT,GPS_LON,GPS_ALT,ROLL,PITCH,YAW,
ERR_DESCENT,ERR_GPS,ERR_SEP,ERR_PARACHUTE
```

**Example:**
```
ISL177115,0001,00:00:12,142.5,98.2,24.3,7.62,9.1,8,30.908200,75.851600,150.2,1.2,-0.8,44.5,0,0,0,0
```

### How to Run

1. Open `cansat_gcs_Project/index.html` in **Google Chrome** or **Microsoft Edge** (required for Web Serial API).
2. No installation or build step — all libraries are bundled locally.
3. **Demo mode:** Click **"Demo Sim: ON"** → **"▶ Start Telemetry"** to stream simulated data without hardware.
4. **Hardware mode:** Flash `arduino/dummy_telemetry.ino` to the WeGyanik Kit, connect USB, click **Connect Serial**, then **Start Telemetry**.

### Key Features

- Offline-capable (vendor libraries bundled; map tiles and fonts load online when available)
- CSV export and graph export
- Packet reset and PC time sync
- Built-in demo telemetry simulator for testing without hardware

---

## Project 2 — Advanced Drone Technology (Guidance & Control)

### Description

Python simulations exploring **PID control**, **Line-of-Sight (LOS) guidance**, and **trajectory tracking** for drones and autonomous boats. Covers altitude hold under wind disturbance, path following with/without water current, and a creative bonus figure-eight drone trajectory.

### Folder Structure

```
Drone_Project/
├── task1_drone_pid.py                      # Task 1: PID altitude control
├── task2_boat_guidance.py                  # Task 2: Boat LOS path tracking
├── bonus_figure_eight_drone.py             # Bonus: Figure-eight trajectory
└── Advanced_Drone_Technology_Project.ipynb # Jupyter notebook (all tasks combined)
```

### Task 1 — PID Drone Altitude Control

| Parameter | Value |
|-----------|-------|
| Target altitude | 10.0 m |
| Wind disturbance | 3.0 m/s² (introduced at t = 6 s) |
| PID gains | Kp = 6.0, Ki = 0.5, Kd = 4.0 |
| Simulation time | 20 s (dt = 0.01 s) |

The drone climbs to and holds 10 m altitude. After 6 seconds a wind disturbance is applied to test disturbance rejection and stability.

**Output:** `pid_tuning_result.png`

### Task 2 — Autonomous Boat Guidance (LOS)

| Parameter | Value |
|-----------|-------|
| Desired path | x = t, y = 4·sin(0.25·t) |
| Controller | P + D heading controller (kp = 1.8, kd = 0.6) |
| Boat speed | 1.2 m/s |
| Lookahead | 6 path indices |

Two cases are simulated:
- **With current:** drift (0.3, 0.2) m/s
- **Without current:** ideal conditions (0, 0) m/s

**Outputs:** `boat_guidance_with_current.png`, `boat_guidance_without_current.png`

### Bonus — Figure-Eight Drone Trajectory

| Parameter | Value |
|-----------|-------|
| Path | Lemniscate of Gerono: x = A·sin(ωt), y = A·sin(ωt)·cos(ωt) |
| Amplitude A | 5.0 m |
| Angular speed ω | 0.4 rad/s |
| Controller | PD position loops (Kp = 8.0, Kd = 5.0) |
| Wind | (0.4, −0.3) m/s² when enabled |

**Output:** `figure_eight_drone_tracking.png`

### How to Run

```bash
cd Drone_Project
python task1_drone_pid.py
python task2_boat_guidance.py
python bonus_figure_eight_drone.py
```

Or open and run `Advanced_Drone_Technology_Project.ipynb` in Jupyter.

---

## Project 3 — Rocketry FEM & CFD Analysis

### Description

Independent Python engineering analysis of a **tapered rocket fin** made from **Aluminium 6061-T6**. Includes a 1D Euler-Bernoulli beam FEM solver (structural), a constant-strength source panel method (inviscid CFD), and a bonus design optimization comparing original vs. optimized geometry.

> **Note:** These Python scripts provide independent engineering estimates. Full 3D FEM and viscous CFD (RANS/k-ω SST) should be run in **SimScale** as required by the assignment.

### Folder Structure

```
Rocketry_Project/
├── fem_fin_analysis.py           # FEM cantilever beam analysis + mesh convergence
├── cfd_fin_panel_method.py       # Inviscid panel method + flow visualization
├── bonus_design_optimization.py  # Original vs optimized fin comparison
├── fem_results_summary.txt       # FEM numerical results
├── cfd_results_summary.txt       # CFD numerical results
└── optimization_comparison.txt   # Optimization comparison table
```

### Fin Geometry (Original Design)

| Parameter | Value |
|-----------|-------|
| Root chord | 150 mm |
| Tip chord | 75 mm |
| Span | 100 mm |
| Thickness | 4.0 mm |
| Material | Aluminium 6061-T6 (E = 68.9 GPa, Yield = 276 MPa) |
| Flight velocity | 100 m/s |
| Dynamic pressure q | 6125 Pa |

### FEM Analysis (`fem_fin_analysis.py`)

- **Method:** 1D Euler-Bernoulli cantilever beam FEM with distributed aerodynamic load
- **Mesh convergence study:** Coarse (4), Medium (16), Fine (64) elements

| Mesh Level | Tip Deflection | Max Root Stress |
|------------|----------------|-----------------|
| Coarse (4 elements) | 0.1507 mm | 6.173 MPa |
| Medium (16 elements) | 0.1475 mm | 7.250 MPa |
| Fine (64 elements) | 0.1474 mm | 7.552 MPa |

| Result | Value |
|--------|-------|
| Max root stress (fine mesh) | **7.552 MPa** |
| Factor of Safety | **36.54** |
| Structural status | **SAFE** |

**Outputs:** `fem_mesh_convergence.png`, `fem_stress_distribution.png`, `fem_results_summary.txt`

### CFD Analysis (`cfd_fin_panel_method.py`)

- **Method:** Constant-strength source panel method on symmetric biconvex fin cross-section
- **Limitation:** Inviscid — cannot capture boundary layer, separation, or wake

| Result | Value |
|--------|-------|
| Reynolds number (chord) | 7.50 × 10⁵ |
| Chord | 112.50 mm |
| Max thickness | 4.00 mm (t/c = 0.036) |
| Min Cp (max suction) | −0.092 |
| Max Cp (stagnation) | 0.140 |
| Estimated Cd | 0.01060 |
| Drag force per unit span | 7.301 N/m |

**Outputs:** `cfd_pressure_distribution.png`, `cfd_streamlines.png`, `cfd_results_summary.txt`

### Bonus — Design Optimization (`bonus_design_optimization.py`)

Compares original vs. optimized fin geometry:

| Change | Original → Optimized |
|--------|----------------------|
| Root chord | 150 mm → 140 mm |
| Tip chord | 75 mm → 70 mm |
| Thickness | 4.0 mm → 4.5 mm |

| Metric | Original | Optimized | Change |
|--------|----------|-----------|--------|
| Max root stress (MPa) | 7.552 | 5.967 | **−21.0%** |
| Tip deflection (mm) | 0.147 | 0.104 | −29.8% |
| Factor of Safety | 36.54 | 46.25 | +26.5% |
| Drag coefficient Cd | 0.0106 | 0.0109 | +2.8% |
| Drag per span (N/m) | 7.301 | 7.004 | −4.1% |
| Mass (g) | 121.5 | 127.6 | +5.0% |

The optimized design reduces root stress significantly with a modest drag and mass trade-off.

**Outputs:** `optimization_comparison.png`, `optimization_comparison.txt`

### How to Run

```bash
cd Rocketry_Project
python fem_fin_analysis.py
python cfd_fin_panel_method.py
python bonus_design_optimization.py
```

---

## Results Summary

### CanSat GCS
- Fully functional single-page ground control dashboard
- Supports demo simulation and real hardware (WeGyanik Kit via Web Serial)
- Real-time telemetry, error codes, graphs, GPS map, 3D orientation, video, and mission control
- CSV and graph export capabilities

### Drone Project
- **Task 1:** PID controller successfully holds 10 m altitude with disturbance rejection after t = 6 s
- **Task 2:** LOS guidance tracks sinusoidal path with and without water current
- **Bonus:** PD controller follows figure-eight (lemniscate) trajectory under wind

### Rocketry Project
- **FEM:** Fin is structurally safe with FoS = 36.54 at 100 m/s (max stress 7.55 MPa vs. 276 MPa yield)
- **CFD:** Inviscid panel method estimates Cd ≈ 0.0106, drag ≈ 7.30 N/m per span
- **Optimization:** Reduced root stress by 21% with optimized chord taper and thickness

---

## How to Run All Projects

| Project | Command / Action |
|---------|------------------|
| CanSat GCS | Open `cansat_gcs_Project/index.html` in Chrome/Edge |
| Drone Task 1 | `python Drone_Project/task1_drone_pid.py` |
| Drone Task 2 | `python Drone_Project/task2_boat_guidance.py` |
| Drone Bonus | `python Drone_Project/bonus_figure_eight_drone.py` |
| Drone Notebook | Open `Drone_Project/Advanced_Drone_Technology_Project.ipynb` |
| Rocketry FEM | `python Rocketry_Project/fem_fin_analysis.py` |
| Rocketry CFD | `python Rocketry_Project/cfd_fin_panel_method.py` |
| Rocketry Bonus | `python Rocketry_Project/bonus_design_optimization.py` |

---

## Dependencies

### CanSat GCS
- **Browser:** Google Chrome or Microsoft Edge (Web Serial API)
- **Libraries:** Chart.js, Leaflet.js, Three.js (bundled in `assets/vendor/`)
- **Hardware (optional):** WeGyanik Kit + Arduino IDE for `dummy_telemetry.ino`

### Drone Project & Rocketry Project
- **Python 3.x**
- **Packages:** `numpy`, `matplotlib`
- **Optional:** Jupyter Notebook (for `.ipynb`)

Install Python dependencies:

```bash
pip install numpy matplotlib jupyter
```

---

## Overall Summary

This repository represents a complete **India Space Lab** portfolio spanning three aerospace engineering domains:

1. **Satellite Operations (CanSat GCS)** — A production-quality web-based ground control station with live telemetry ingestion, visualization, error monitoring, GPS tracking, 3D attitude display, and mission command capabilities. Designed for both hardware-in-the-loop testing and standalone demo operation.

2. **Autonomous Systems (Drone Project)** — Foundational control theory applied through Python simulations: PID altitude hold with disturbance rejection, Line-of-Sight guidance for path tracking under environmental disturbances, and advanced figure-eight trajectory following. Demonstrates understanding of feedback control, guidance laws, and trajectory planning.

3. **Structural & Aerodynamic Engineering (Rocketry Project)** — Rigorous engineering analysis of a rocket fin using finite element methods (beam FEM with mesh convergence) and computational fluid dynamics (inviscid panel method with empirical drag estimation). Includes a design optimization study balancing structural safety, aerodynamic drag, and mass.

All three projects were developed independently in Python and JavaScript, produce reproducible numerical results and visual outputs, and align with ISL assignment requirements for the CanSat/CubeSat, Advanced Drone Technology, and Rocketry modules.

---

*For detailed CanSat GCS documentation, see [`cansat_gcs_Project/docs/README.md`](cansat_gcs_Project/docs/README.md).*
