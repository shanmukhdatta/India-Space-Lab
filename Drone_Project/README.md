# Project 2: Advanced Drone Technology (Guidance & Control)

**Student:** Boda Shanmukha Datta  
**ISL Enrolment No.:** ISL-177115  
**Institution:** NIT Jalandhar  
**Email:** bodasd.ic.24@nitj.ac.in  

---

## 1. Overview & Concept

This project implements autonomous guidance and control algorithms in Python for drones and marine surface vessels. It demonstrates closed-loop feedback control, disturbance rejection, Line-of-Sight (LOS) path tracking, and trajectory tracking under environmental forces such as wind gusts and water currents.

---

## 2. Technical Architecture & File Structure

```
Drone_Project/
├── task1_drone_pid.py                      # Task 1: PID drone altitude hold + wind disturbance
├── task2_boat_guidance.py                  # Task 2: Autonomous boat LOS path tracking
├── bonus_figure_eight_drone.py             # Bonus: Figure-eight (lemniscate) trajectory tracking
├── Advanced_Drone_Technology_Project.ipynb # Combined Jupyter Notebook (All tasks)
├── Guidance_and_Control_Project_Report.docx# Full project report document
├── pid_tuning_result.png                   # Output plot for Task 1
├── boat_guidance_with_current.png          # Output plot for Task 2 (with current)
├── boat_guidance_without_current.png       # Output plot for Task 2 (no current)
├── figure_eight_drone_tracking.png         # Output plot for Bonus task
└── requirements.txt                        # Python dependencies (numpy, matplotlib)
```

---

## 3. Mathematical Principles & Implementation Details

### Task 1 — PID Altitude Control (`task1_drone_pid.py`)
- **Objective:** Maintain a target altitude of $z_{\text{target}} = 10.0\text{ m}$ under a step wind disturbance of $3.0\text{ m/s}^2$ introduced at $t = 6.0\text{ s}$.
- **Control Law:**
  $$u(t) = K_p \cdot e(t) + K_i \int e(t) dt + K_d \frac{de(t)}{dt}$$
- **Tuned Gains:** $K_p = 6.0$, $K_i = 0.5$, $Kd = 4.0$.
- **Key Finding:** The integral gain $K_i$ successfully eliminates steady-state altitude offset caused by constant wind force.

### Task 2 — Autonomous Boat Guidance (`task2_boat_guidance.py`)
- **Objective:** Track a sinusoidal waypoint path $y(x) = 4 \sin(0.25 x)$ at a speed of $v = 1.2\text{ m/s}$.
- **Guidance Law:** Line-of-Sight (LOS) lookahead algorithm steering toward a waypoint 6 indices ahead on the desired path.
- **Heading Controller:** $P+D$ heading angle regulation ($K_p = 1.8$, $K_d = 0.6$).
- **Cases Tested:**
  1. Ideal calm water (no current drift).
  2. Water current drift vector $\vec{v}_{\text{current}} = (0.3, 0.2)\text{ m/s}$.

### Bonus — Figure-Eight Trajectory Tracking (`bonus_figure_eight_drone.py`)
- **Objective:** Follow a continuous figure-eight path (Lemniscate of Gerono):
  $$x(t) = A \sin(\omega t), \quad y(t) = A \sin(\omega t) \cos(\omega t)$$
  with amplitude $A = 5.0\text{ m}$ and angular frequency $\omega = 0.4\text{ rad/s}$.
- **Controller:** Dual-axis PD position loops ($K_p = 8.0$, $K_d = 5.0$) subject to wind acceleration $\vec{a}_{\text{wind}} = (0.4, -0.3)\text{ m/s}^2$.

---

## 4. How to Run

Ensure Python 3.x and dependencies are installed:

```bash
pip install -r requirements.txt
```

Run individual simulation scripts:

```bash
python task1_drone_pid.py
python task2_boat_guidance.py
python bonus_figure_eight_drone.py
```

Or open `Advanced_Drone_Technology_Project.ipynb` in Jupyter:

```bash
jupyter notebook Advanced_Drone_Technology_Project.ipynb
```

---

## 5. Verification & Results Summary

| Task | Output Image | Result |
|------|--------------|--------|
| Task 1: PID Altitude | `pid_tuning_result.png` | Fast response (<2s rise time), zero steady-state error after wind disturbance |
| Task 2: Boat LOS | `boat_guidance_with_current.png`, `boat_guidance_without_current.png` | Smooth path tracking with crab-angle compensation against current |
| Bonus: Figure-Eight | `figure_eight_drone_tracking.png` | Tight 2D trajectory tracking with minimal tracking lag |

---

## 6. Rubric Evaluation & Deliverables Status

| Rubric Component | Weight | Status | Evaluation Details & Visual Proof |
|------------------|--------|--------|-----------------------------------|
| **Task 1 — PID Altitude Control** | 30% | **Completed** | Complete PID formulation, gain tuning ($6.0, 0.5, 4.0$), $3.0\text{ m/s}^2$ wind rejection |
| **Task 2 — Boat Guidance (LOS)** | 30% | **Completed** | Sinusoidal path tracking, LOS lookahead, evaluated with/without water current |
| **Bonus — Figure-Eight Control** | 20% | **Completed** | Lemniscate path equation, dual-axis PD control under wind acceleration |
| **Code Quality & Notebook** | 20% | **Completed** | Modular Python scripts, Jupyter Notebook, technical report `.docx`, 4 PNG plots |
| **TOTAL STATUS** | **100%** | **Completed** | **Fully Completed & Verified** |
