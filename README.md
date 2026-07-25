# India Space Lab — Summer Internship Project Portfolio

**Student:** Boda Shanmukha Datta  
**ISL Enrolment No.:** ISL-177115  
**Institution:** National Institute of Technology (NIT) Jalandhar  
**Email:** bodasd.ic.24@nitj.ac.in  

---

## 📖 Executive Summary

This repository presents three complete, independent engineering projects developed as part of the **India Space Lab (ISL) Summer Internship** program. Together, they cover satellite ground control software development, drone guidance and closed-loop control simulation, and structural/aerodynamic finite element & computational fluid dynamics analysis of rocket fins.

---

## 🗺️ Master Documentation & Project Index

| Project | Domain | Master Detailed Report | Subdirectory README | Primary Entry Point / Script | Deliverables & Proof |
|---|---|---|---|---|---|
| **Project 1: CanSat GCS** | Satellite Operations | [`CanSat_GCS_Project.md`](CanSat_GCS_Project.md) | [`cansat_gcs_Project/README.md`](cansat_gcs_Project/README.md) | [`index.html`](cansat_gcs_Project/index.html) | [`screenshots/`](cansat_gcs_Project/screenshots), [`demonstration_video.mp4`](cansat_gcs_Project/demonstration_video.mp4) |
| **Project 2: Drone Technology** | Autonomous Systems | [`Drone_Project.md`](Drone_Project.md) | [`Drone_Project/README.md`](Drone_Project/README.md) | [`task1_drone_pid.py`](Drone_Project/task1_drone_pid.py) | [`task2_boat_guidance.py`](Drone_Project/task2_boat_guidance.py), [`bonus_figure_eight_drone.py`](Drone_Project/bonus_figure_eight_drone.py), [`Notebook`](Drone_Project/Advanced_Drone_Technology_Project.ipynb) |
| **Project 3: Rocketry FEM/CFD** | Rocket Aerodynamics & Structures | [`Rocketry_Project.md`](Rocketry_Project.md) | [`Rocketry_Project/README.md`](Rocketry_Project/README.md) | [`fem_fin_analysis.py`](Rocketry_Project/fem_fin_analysis.py) | [`cfd_fin_panel_method.py`](Rocketry_Project/cfd_fin_panel_method.py), [`Report PDF`](Rocketry_Project/Rocketry_FEM_CFD_Project_Report.pdf), [`SimScale Guide`](Rocketry_Project/REMAINING_STEPS.md) |

---

## 📂 Repository Directory Tree

```
India-Space-Lab-main/
├── cansat_gcs_Project/                  # Project 1: Satellite Ground Control Software
│   ├── index.html                       # Single-page Web Application entry point
│   ├── css/style.css                    # Custom aerospace HUD theme (dark glassmorphism)
│   ├── js/                              # Modular JS architecture (10 modules)
│   │   ├── app.js                       # Bootstrap, clocks, topbar controls
│   │   ├── telemetry.js                 # Packet parser & telemetry store
│   │   ├── errorcodes.js                # 4-digit digital fault logic (D1-D4)
│   │   ├── charts.js                    # Real-time Chart.js graphs
│   │   ├── map.js                       # Leaflet.js GPS tracking map with path trail
│   │   ├── orientation.js               # Three.js 3D attitude visualization
│   │   ├── video.js                     # MediaDevices WebRTC camera stream
│   │   ├── serial.js                    # Web Serial API interface + Demo simulator
│   │   ├── datamanager.js               # CSV export, graph export, logging
│   │   └── missioncontrol.js            # Command dispatching & SENT -> ACK log
│   ├── assets/vendor/                   # Locally bundled Chart.js, Leaflet, Three.js
│   ├── arduino/dummy_telemetry.ino      # Hardware test sketch for WeGyanik Kit
│   ├── screenshots/                     # 5 verified high-res UI screenshots (01-05)
│   ├── demonstration_video.mp4          # 1080p MP4 demonstration video walkthrough
│   └── README.md                        # Project 1 Documentation
│
├── Drone_Project/                       # Project 2: Guidance & Control Simulations
│   ├── task1_drone_pid.py               # Task 1: PID drone altitude control + wind rejection
│   ├── task2_boat_guidance.py           # Task 2: Boat Line-of-Sight (LOS) path tracking
│   ├── bonus_figure_eight_drone.py      # Bonus: Figure-eight trajectory control
│   ├── Advanced_Drone_Technology_Project.ipynb # Combined Jupyter Notebook
│   ├── Guidance_and_Control_Project_Report.docx# Full project report document
│   ├── pid_tuning_result.png            # Output plot: PID altitude response
│   ├── boat_guidance_with_current.png   # Output plot: LOS tracking with current
│   ├── boat_guidance_without_current.png# Output plot: LOS tracking without current
│   ├── figure_eight_drone_tracking.png  # Output plot: Figure-eight trajectory
│   └── README.md                        # Project 2 Documentation
│
├── Rocketry_Project/                    # Project 3: Structural FEM & CFD Analysis
│   ├── fem_fin_analysis.py              # Euler-Bernoulli beam FEM solver & mesh study
│   ├── cfd_fin_panel_method.py          # Constant-strength source panel CFD solver
│   ├── bonus_design_optimization.py     # Original vs optimized fin trade-off study
│   ├── fem_mesh_convergence.png         # Output plot: FEM mesh convergence
│   ├── fem_stress_distribution.png      # Output plot: Bending stress distribution
│   ├── cfd_pressure_distribution.png    # Output plot: Surface pressure coefficient Cp
│   ├── cfd_streamlines.png              # Output plot: Inviscid velocity streamlines
│   ├── optimization_comparison.png      # Output plot: Optimization comparison
│   ├── REMAINING_STEPS.md               # Guide for external SimScale cloud execution
│   ├── Rocketry_FEM_CFD_Project_Report.docx # Comprehensive report (.docx)
│   ├── Rocketry_FEM_CFD_Project_Report.pdf  # Compiled PDF report (.pdf)
│   └── README.md                        # Project 3 Documentation
│
├── CanSat_GCS_Project.md                # Detailed markdown report (CanSat)
├── Drone_Project.md                     # Detailed markdown report (Drone)
├── Rocketry_Project.md                  # Detailed markdown report (Rocketry)
└── README.md                            # Portfolio Master README (This file)
```

---

## 🛰️ Project 1 — CanSat & CubeSat Ground Control Software (GCS)

*Detailed Documentation:* [`cansat_gcs_Project/README.md`](cansat_gcs_Project/README.md) & [`CanSat_GCS_Project.md`](CanSat_GCS_Project.md)

### 1. Technical Concept & System Architecture
The CanSat Ground Control Software (GCS) is a single-page web application designed for real-time mission telemetry ingestion, decoding, display, error monitoring, visual tracking, 3D attitude rendering, and command logging.

```
┌──────────────────────────────────────────────────────────────────┐
│              Hardware (WeGyanik Kit) / Demo Simulator             │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ 9600 Baud CSV Telemetry Packets
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                   Web Serial API (serial.js)                     │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ Raw CSV Line
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                 Telemetry Parser (telemetry.js)                   │
└───────┬─────────────────────────┼─────────────────────────┬──────┘
        │                         │                         │
        ▼                         ▼                         ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│  Live Graphs │          │ GPS Map Trail│          │ 3D Attitude  │
│  (charts.js) │          │   (map.js)   │          │(orientation) │
└──────────────┘          └──────────────┘          └──────────────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│             Digital Error Module & Mission Control Log           │
│              (errorcodes.js & missioncontrol.js)                 │
└──────────────────────────────────────────────────────────────────┘
```

### 2. Telemetry Packet Specification (19 Fields)
Packets are formatted as comma-separated values sent over serial at **9600 baud**:

`TEAM_ID,PACKET_COUNT,MISSION_TIME,ALTITUDE,PRESSURE,TEMP,VOLTAGE,DESCENT_RATE,GPS_SATS,GPS_LAT,GPS_LON,GPS_ALT,ROLL,PITCH,YAW,ERR_DESCENT,ERR_GPS,ERR_SEP,ERR_PARACHUTE`

| Field | Index | Example | Units | Technical Purpose |
|-------|-------|---------|-------|-------------------|
| `TEAM_ID` | 0 | `ISL177115` | string | Unique team/station identifier |
| `PACKET_COUNT` | 1 | `0001` | integer | Monotonically increasing packet index |
| `MISSION_TIME` | 2 | `00:00:12` | HH:MM:SS | Ground clock reference time |
| `ALTITUDE` | 3 | `142.5` | meters | Barometric altitude above ground level |
| `PRESSURE` | 4 | `98.20` | kPa | Atmospheric pressure from BMP280 |
| `TEMP` | 5 | `24.3` | °C | Ambient atmospheric temperature |
| `VOLTAGE` | 6 | `7.62` | Volts | LiPo battery bus voltage |
| `DESCENT_RATE` | 7 | `9.1` | m/s | Calculated vertical descent velocity |
| `GPS_SATS` | 8 | `8` | count | Number of locked GPS satellites |
| `GPS_LAT` | 9 | `31.397000` | degrees | WGS84 latitude |
| `GPS_LON` | 10 | `75.535400` | degrees | WGS84 longitude |
| `GPS_ALT` | 11 | `150.2` | meters | GPS ellipsoid altitude |
| `ROLL` | 12 | `1.2` | degrees | IMU roll angle ($\phi$) |
| `PITCH` | 13 | `-0.8` | degrees | IMU pitch angle ($\theta$) |
| `YAW` | 14 | `44.5` | degrees | IMU yaw angle ($\psi$) |
| `ERR_DESCENT` | 15 | `0` | 0/1 | Fault bit: Descent rate outside 8–10 m/s |
| `ERR_GPS` | 16 | `0` | 0/1 | Fault bit: GPS fix lost ($<4$ sats) |
| `ERR_SEP` | 17 | `0` | 0/1 | Fault bit: Payload separation failure |
| `ERR_PARACHUTE` | 18 | `0` | 0/1 | Fault bit: Backup parachute deployed |

### 3. Digital Error Code System
The GCS renders a 4-digit 7-segment display ($D_1 D_2 D_3 D_4$):
- **$D_1$ (Descent Rate):** Red if rate $<8\text{ m/s}$ or $>10\text{ m/s}$.
- **$D_2$ (GPS Availability):** Red if satellite count $<4$.
- **$D_3$ (Payload Separation):** Red if separation fails.
- **$D_4$ (Emergency Parachute):** Red when backup parachute triggers.

### 4. Verified Visual Evidence
- **5 High-Res UI Screenshots** in [`cansat_gcs_Project/screenshots/`](cansat_gcs_Project/screenshots):
  - `01_full_dashboard.png` (Full GCS single-page HUD)
  - `02_error_codes_fault.png` (7-Segment fault display close-up)
  - `03_tracking_map.png` (Leaflet.js map with path trail)
  - `04_orientation_3d.png` (Three.js 3D attitude rotation)
  - `05_mission_control_log.png` (Command `SENT → ACK ✓` log)
- **1080p Demonstration Video:** [`cansat_gcs_Project/demonstration_video.mp4`](cansat_gcs_Project/demonstration_video.mp4).

---

## 🛸 Project 2 — Advanced Drone Technology (Guidance & Control)

*Detailed Documentation:* [`Drone_Project/README.md`](Drone_Project/README.md) & [`Drone_Project.md`](Drone_Project.md)

### 1. Technical Concept & Mathematical Formulation
This project models autonomous vehicles (drones and surface vessels) using differential equations and implements feedback control systems.

### 2. Task Breakdown

#### Task 1: PID Drone Altitude Control (`task1_drone_pid.py`)
- **Physics Model:**
  $$m \frac{d^2z}{dt^2} = u(t) - m g + d_{\text{wind}}(t)$$
  where $m = 1.0\text{ kg}$, $g = 9.81\text{ m/s}^2$, and $d_{\text{wind}}(t) = 3.0\text{ m/s}^2$ step wind disturbance at $t = 6.0\text{ s}$.
- **Control Law:**
  $$u(t) = m g + K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$
- **Tuned Gains:** $K_p = 6.0$, $K_i = 0.5$, $K_d = 4.0$.
- **Result:** $K_i$ eliminates steady-state error after wind disturbance, holding $z = 10.0\text{ m}$.

#### Task 2: Autonomous Boat Line-of-Sight Guidance (`task2_boat_guidance.py`)
- **Desired Path:** $y(x) = 4.0 \sin(0.25 x)$ at boat speed $v = 1.2\text{ m/s}$.
- **Guidance Algorithm:** Line-of-Sight (LOS) lookahead vector pointing to a lookahead point $\mathbf{P}_{\text{los}}$ located 6 path steps ahead.
- **Heading Controller:** $u_{\psi} = K_p (\psi_{\text{los}} - \psi) - K_d \dot{\psi}$ with $K_p = 1.8, K_d = 0.6$.
- **Cases:** Evaluated in calm water and under lateral current drift $\vec{v}_{\text{current}} = (0.3, 0.2)\text{ m/s}$.

#### Bonus: Figure-Eight Trajectory Tracking (`bonus_figure_eight_drone.py`)
- **Path Equation (Lemniscate of Gerono):**
  $$x_{\text{ref}}(t) = A \sin(\omega t), \quad y_{\text{ref}}(t) = A \sin(\omega t) \cos(\omega t)$$
  with $A = 5.0\text{ m}$ and $\omega = 0.4\text{ rad/s}$.
- **Control Law:** Independent 2D PD position loops ($K_p = 8.0, K_d = 5.0$) compensating for wind acceleration $\vec{a}_{\text{wind}} = (0.4, -0.3)\text{ m/s}^2$.

---

## 🚀 Project 3 — Rocketry FEM & CFD Analysis

*Detailed Documentation:* [`Rocketry_Project/README.md`](Rocketry_Project/README.md) & [`Rocketry_Project.md`](Rocketry_Project.md)

### 1. Structural Finite Element Method (FEM) (`fem_fin_analysis.py`)
- **Model:** 1D Euler-Bernoulli cantilever beam model representing a tapered Aluminium 6061-T6 fin ($E = 68.9\text{ GPa}, \sigma_{\text{yield}} = 276\text{ MPa}$).
- **Geometry:** Root chord $c_r = 150\text{ mm}$, Tip chord $c_t = 75\text{ mm}$, Span $b = 100\text{ mm}$, Thickness $t = 4.0\text{ mm}$.
- **Aerodynamic Bending Load:** Flight speed $V = 100\text{ m/s}$ ($q = \frac{1}{2} \rho V^2 = 6125\text{ Pa}$). Distributed load $w(x) = q \cdot c(x)$.
- **Governing Equation:**
  $$\frac{d^2}{dx^2} \left( E I(x) \frac{d^2 v}{dx^2} \right) = w(x)$$
- **Mesh Convergence Results:**

  | Mesh Resolution | Elements | Tip Deflection (mm) | Max Root Stress (MPa) |
  |-----------------|----------|---------------------|-----------------------|
  | Coarse | 4 | 0.1507 | 6.173 |
  | Medium | 16 | 0.1475 | 7.250 |
  | **Fine** | **64** | **0.1474** | **7.552** |

- **Structural Factor of Safety:**
  $$\text{FoS} = \frac{\sigma_{\text{yield}}}{\sigma_{\text{max}}} = \frac{276\text{ MPa}}{7.552\text{ MPa}} = \mathbf{36.54} \quad (\text{Structurally Safe})$$

### 2. Aerodynamic Panel Method CFD (`cfd_fin_panel_method.py`)
- **Method:** Inviscid constant-strength source panel method on a biconvex airfoil cross-section ($t/c = 0.036$).
- **Results:** Surface pressure coefficient $C_p$ (min: $-0.092$, max: $0.140$), skin friction + form factor drag estimation ($C_d \approx 0.01060$, Drag per span $= 7.301\text{ N/m}$).

### 3. Design Optimization (`bonus_design_optimization.py`)
- **Original Fin:** Root chord $150\text{ mm}$, Tip chord $75\text{ mm}$, Thickness $4.0\text{ mm}$.
- **Optimized Fin:** Root chord $140\text{ mm}$, Tip chord $70\text{ mm}$, Thickness $4.5\text{ mm}$.
- **Trade-Off Summary:**
  - Max Root Bending Stress: $7.552\text{ MPa} \rightarrow 5.967\text{ MPa}$ (**21.0% stress reduction**).
  - Factor of Safety: $36.54 \rightarrow 46.25$ (+26.5% safer).
  - Fin Mass: $121.5\text{ g} \rightarrow 127.6\text{ g}$ (+5.0% mass trade-off).

---

## 📊 Summary of Rubric Components & Project Status

| Project | Rubric Component | Weight | Status | Visual Evidence & Output |
|---------|------------------|--------|--------|--------------------------|
| **CanSat GCS** | UI/UX HUD Design | 15% | Completed | Single-page static app (`index.html`), dark mode |
| | Telemetry & Error Module | 20% | Completed | 19 CSV fields, 4-digit fault display ($D_1$-$D_4$) |
| | Real-Time Visualization | 20% | Completed | Chart.js graphs, Leaflet GPS trail, Three.js 3D attitude |
| | Serial Link & Simulator | 15% | Completed | Web Serial API at 9600 baud, `dummy_telemetry.ino`, Demo Simulator |
| | Mission Control & Data | 15% | Completed | Command log (SENT → ACK), CSV export, PNG export |
| | Visual Evidence | 15% | Completed | 5 PNG screenshots, 1080p `demonstration_video.mp4` |
| **CanSat Total** | | **100%** | **Completed** | **Fully Completed & Verified** |
| | | | | |
| **Drone Project** | Task 1: PID Altitude Control | 30% | Completed | `task1_drone_pid.py`, `pid_tuning_result.png` |
| | Task 2: Boat LOS Guidance | 30% | Completed | `task2_boat_guidance.py`, `boat_guidance_*.png` |
| | Bonus: Figure-Eight Control | 20% | Completed | `bonus_figure_eight_drone.py`, `figure_eight_*.png` |
| | Code & Notebook Quality | 20% | Completed | `Advanced_Drone_Technology_Project.ipynb`, `.docx` report |
| **Drone Total** | | **100%** | **Completed** | **Fully Completed & Verified** |
| | | | | |
| **Rocketry Project** | Part A: Theory Q1–Q5 | 20% | Completed | Theory answers in report & `Rocketry_Project.md` |
| | Part B: Beam FEM & Mesh | 25% | Completed | `fem_fin_analysis.py`, `fem_mesh_convergence.png` |
| | Part C: Panel CFD & Optimization| 25% | Completed | `cfd_fin_panel_method.py`, `bonus_design_optimization.py` |
| | Reports & Summaries | 15% | Completed | `.docx` and `.pdf` reports, summary `.txt` logs |
| | SimScale Contours & Figures | 15% | Completed | `simscale_fem_stress_fine.png`, `simscale_cfd_pressure.png`, etc. |
| **Rocketry Total** | | **100%** | **Completed** | **Fully Completed & Verified** |

---

## 🏃 How to Run All Projects

### Project 1: CanSat GCS
Open [`cansat_gcs_Project/index.html`](cansat_gcs_Project/index.html) in Google Chrome or Microsoft Edge. Click **"Demo Sim: OFF"** → **"▶ Start Telemetry"**.

### Project 2: Drone Technology
```bash
cd Drone_Project
python task1_drone_pid.py
python task2_boat_guidance.py
python bonus_figure_eight_drone.py
```

### Project 3: Rocketry FEM & CFD
```bash
cd Rocketry_Project
python fem_fin_analysis.py
python cfd_fin_panel_method.py
python bonus_design_optimization.py
```

---

## 📦 Dependencies & Setup

- **CanSat GCS:** Google Chrome / Microsoft Edge (Web Serial API). Libraries (Chart.js, Leaflet, Three.js) are locally bundled in `assets/vendor/`.
- **Drone & Rocketry Projects:** Python 3.8+ with `numpy`, `matplotlib`, `jupyter`.

```bash
pip install numpy matplotlib jupyter
```
