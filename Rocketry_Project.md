# Rocketry FEM & CFD Analysis Project — Detailed Project Report

**Student:** Boda Shanmukha Datta  
**ISL Enrolment No.:** ISL-177115  
**Institution:** NIT Jalandhar  
**Email:** bodasd.ic.24@nitj.ac.in  

---

## 1. What Is This Project?

This project analyzes a **rocket fin** — the flat wing-like surface on a rocket that provides stability during flight. We answer two critical engineering questions:

1. **Will the fin break?** (Structural analysis using FEM — Finite Element Method)
2. **How much drag does the fin create?** (Aerodynamic analysis using CFD — Computational Fluid Dynamics)

We also perform a **design optimization** to improve the fin by reducing stress while managing drag and weight trade-offs.

> **Note:** The Python scripts here provide independent engineering estimates. Full 3D analysis should also be done in **SimScale** (cloud simulation platform) as required by the assignment.

---

## 2. Theoretical Background (Beginner Explanation)

### 2.1 What Is a Rocket Fin?

A rocket fin is a thin, flat surface attached to the rocket body. During flight, air pushes against the fin. This creates:
- **Lift** — keeps the rocket stable (pointing forward)
- **Drag** — slows the rocket down (undesirable)
- **Bending force** — can bend or break the fin (structural concern)

```
        Air flow →  ┌──────┐
                    │ Fin  │ ← bends like a diving board
                    │      │
                    └──────┘
                    ████████ ← Rocket body (fixed/root)
```

The fin is **fixed at the root** (where it attaches to the rocket) and **free at the tip** — like a diving board fixed at one end.

### 2.2 What Is FEM (Finite Element Method)?

**FEM** divides a complex structure into many small simple pieces called **elements**. Each element is easy to analyze mathematically. Combined together, they approximate the behavior of the whole structure.

**Why use FEM?**
- Real fins have complex shapes — hard to solve by hand
- FEM gives stress, deflection, and safety factor numerically
- Industry standard for structural design (bridges, aircraft, rockets)

**Key FEM concepts:**

| Term | Meaning | Analogy |
|------|---------|---------|
| **Node** | Point on the structure | Joint in a skeleton |
| **Element** | Piece between two nodes | Bone between joints |
| **Mesh** | All nodes + elements together | Full skeleton |
| **Boundary condition** | What's fixed/movable | Feet planted on ground |
| **Load** | Force applied | Weight on your back |
| **Stress** | Force per unit area | How much a material is "squeezed/stretched" |
| **Deflection** | How much it bends | How far the diving board tip moves down |
| **Factor of Safety (FoS)** | Yield strength ÷ max stress | "How many times stronger than needed" |

**Our approach:** We model the fin as a **1D cantilever beam** (simplification) using **Euler-Bernoulli beam theory** — the classic engineering method for bending beams.

### 2.3 Euler-Bernoulli Beam Theory

When a beam bends:
- Top surface is **compressed** (pushed together)
- Bottom surface is **stretched** (pulled apart)
- Neutral axis in the middle has zero stress

**Key equation:**
```
M = E × I × (d²v/dx²)
```

Where:
- M = bending moment (Nm)
- E = Young's modulus (material stiffness)
- I = second moment of area (cross-section shape)
- v = deflection

**Stress at any point:**
```
σ = M × y / I
```

Where y = distance from neutral axis.

### 2.4 What Is CFD (Computational Fluid Dynamics)?

**CFD** simulates how fluid (air) flows around an object. It answers:
- Where is air pressure high/low?
- Where does flow speed up or slow down?
- How much drag force is created?

**Our approach:** We use a **panel method** — a simplified inviscid (frictionless) flow solver. It gives pressure distribution but cannot capture:
- Boundary layer (thin slow air near surface)
- Flow separation (air detaching from surface)
- Wake (turbulent region behind object)

For accurate drag, viscous CFD (RANS/k-ω SST) in SimScale is required.

### 2.5 Key Aerodynamic Concepts

| Term | Symbol | Meaning |
|------|--------|---------|
| Dynamic pressure | q = ½ρV² | "Force" of air at speed V |
| Pressure coefficient | Cp | Normalized pressure (Cp=1 at stagnation, Cp<0 where air speeds up) |
| Drag coefficient | Cd | How "draggy" the shape is (lower = better) |
| Reynolds number | Re = V×c/ν | Ratio of inertial to viscous forces (predicts laminar vs turbulent) |

### 2.6 Factor of Safety

```
FoS = Yield Strength / Maximum Stress
```

| FoS | Meaning |
|-----|---------|
| FoS > 1 | Structure won't yield (permanent deformation) |
| FoS > 1.5 | Typical minimum for aerospace |
| FoS > 3 | Conservative/safe design |
| FoS < 1 | Structure will fail — UNSAFE |

---

## 3. Tasks Given (Assignment Requirements)

| # | Task | Description | File |
|---|------|-------------|------|
| 1 | Fin Geometry & Material | Define dimensions and Aluminium 6061-T6 properties | `fem_fin_analysis.py` |
| 2 | Boundary Conditions | Apply aerodynamic load at V = 100 m/s | `fem_fin_analysis.py`, `cfd_fin_panel_method.py` |
| 3 | Mesh Convergence Study | Coarse (4), Medium (16), Fine (64) elements | `fem_fin_analysis.py` |
| 4 | Flow Visualization | Pressure distribution and streamlines | `cfd_fin_panel_method.py` |
| 5 | Results & Discussion | Stress, deflection, FoS, drag coefficient | Both scripts + `.txt` summaries |
| 6 | Bonus: Design Optimization | Compare original vs. optimized fin geometry | `bonus_design_optimization.py` |

---

## 4. Fin Design Parameters

### 4.1 Original Design

| Parameter | Value | Description |
|-----------|-------|-------------|
| Root chord | 150 mm | Width at base (attached to rocket) |
| Tip chord | 75 mm | Width at tip (free end) |
| Span | 100 mm | Length from root to tip |
| Thickness | 4.0 mm | Uniform thickness |
| Material | Aluminium 6061-T6 | E = 68.9 GPa, Yield = 276 MPa, ρ = 2700 kg/m³ |
| Flight velocity | 100 m/s | Assumed max dynamic pressure phase |
| Air density | 1.225 kg/m³ | Sea level standard |

### 4.2 Fin Shape

The fin is a **tapered trapezoid** — wider at the root, narrower at the tip:

```
    Tip (75mm)
    ┌──────────┐
    │          │  ← 100mm span
    │          │
    └──────────┘
    Root (150mm)
    ════════════ Rocket body
```

Cross-section is a thin **symmetric biconvex (diamond) profile** for CFD analysis.

---

## 5. Task 1–3 — FEM Structural Analysis

### 5.1 Problem Statement

Will the rocket fin survive aerodynamic loading at 100 m/s? Calculate stress, deflection, and factor of safety.

### 5.2 How I Executed the FEM Analysis

**Step 1 — Defined geometry and material:**
```python
root_chord = 0.150 m    # 150 mm
tip_chord = 0.075 m     # 75 mm
span = 0.100 m          # 100 mm
thickness = 0.004 m     # 4 mm
E = 68.9 × 10⁹ Pa       # Young's modulus
yield_strength = 276 × 10⁶ Pa  # 276 MPa
```

**Step 2 — Calculated aerodynamic load:**
```python
V = 100 m/s
ρ = 1.225 kg/m³
q = ½ × ρ × V² = 6125 Pa (dynamic pressure)

# Distributed load per unit span at position x:
w(x) = q × chord(x)
# where chord(x) tapers linearly from 150mm to 75mm
```

**Step 3 — Built FEM solver (Euler-Bernoulli beam elements):**

Each element is a 2-node beam with 4 degrees of freedom (deflection + rotation at each node).

For each element:
1. Calculate stiffness matrix `[K]` (depends on E, I, element length)
2. Calculate load vector `{F}` (from distributed aerodynamic pressure)
3. Assemble into global system
4. Apply boundary condition: root fixed (deflection = 0, rotation = 0)
5. Solve: `[K]{d} = {F}` for unknown displacements
6. Recover bending moments and stresses

**Step 4 — Mesh convergence study (Task 3):**

| Mesh | Elements | Tip Deflection | Max Root Stress |
|------|----------|----------------|-----------------|
| Coarse | 4 | 0.1507 mm | 6.173 MPa |
| Medium | 16 | 0.1475 mm | 7.250 MPa |
| Fine | 64 | 0.1474 mm | 7.552 MPa |

**Why mesh convergence matters:**
- Coarse mesh (4 elements) → inaccurate results
- Fine mesh (64 elements) → results stop changing → **converged solution**
- Tip deflection changed only 0.0001 mm from medium to fine → mesh is adequate

**Step 5 — Calculated Factor of Safety:**
```
FoS = 276 MPa / 7.552 MPa = 36.54
Status: SAFE (well above minimum FoS of 1.5)
```

**Step 6 — Generated outputs:**
- `fem_mesh_convergence.png` — plot showing convergence with mesh refinement
- `fem_stress_distribution.png` — stress along fin span
- `fem_results_summary.txt` — numerical results

### 5.3 FEM Results Summary

| Result | Value |
|--------|-------|
| Dynamic pressure | 6125 Pa |
| Max root stress | **7.552 MPa** |
| Tip deflection | **0.1474 mm** |
| Yield strength | 276 MPa |
| Factor of Safety | **36.54** |
| Status | **SAFE** |

**Interpretation for beginners:**
- The fin experiences only 7.55 MPa of stress, but the material can handle 276 MPa
- The fin is **36 times stronger than it needs to be** — very safe
- Maximum stress occurs at the **root** (where fin meets rocket body) — expected, like a diving board bends most at the wall
- Tip deflection of 0.15 mm is tiny — the fin barely bends

---

## 6. Task 4–5 — CFD Aerodynamic Analysis

### 6.1 Problem Statement

What is the airflow pattern around the fin cross-section? What is the estimated drag?

### 6.2 How I Executed the CFD Analysis

**Step 1 — Defined fin cross-section:**
```python
chord = 112.5 mm     # average chord
t_max = 4.0 mm       # max thickness
# Symmetric biconvex (parabolic arc) profile
```

**Step 2 — Applied flow conditions:**
```python
V_inf = 100 m/s      # freestream velocity
Re = V × chord / ν = 7.50 × 10⁵  # Reynolds number
```

**Step 3 — Panel method solver:**

The fin surface is divided into ~160 panels. For each panel:
1. Place a source (fluid injection) on the panel
2. Solve for source strength that makes flow tangent to surface (no flow through wall)
3. Calculate pressure coefficient: Cp = 1 - (V_local/V_inf)²

**Step 4 — Generated flow visualizations:**
- `cfd_pressure_distribution.png` — Cp vs. x/chord
- `cfd_streamlines.png` — velocity field with streamlines around fin

**Step 5 — Estimated drag (empirical):**
```python
# Skin friction (turbulent flat plate):
Cf = 0.074 / Re^0.2 = 0.00495

# Form factor (thickness correction):
FF = 1 + 2×(t/c) + 60×(t/c)⁴ = 1.0712

# Total drag coefficient (both surfaces):
Cd = Cf × FF × 2 = 0.01060

# Drag force per unit span:
Drag = Cd × q × chord = 7.301 N/m
```

**Step 6 — Saved `cfd_results_summary.txt`**

### 6.3 CFD Results Summary

| Result | Value |
|--------|-------|
| Reynolds number | 7.50 × 10⁵ |
| Min Cp (max suction) | −0.092 |
| Max Cp (stagnation) | 0.140 |
| Estimated Cd | **0.01060** |
| Drag per unit span | **7.301 N/m** |

**Interpretation for beginners:**
- Air speeds up over the thickest part of the fin → low pressure (suction, Cp = −0.092)
- Air stops at leading/trailing edges → high pressure (stagnation, Cp = 0.140)
- Drag coefficient Cd = 0.0106 is relatively low (thin fin = less drag)
- This is an **estimate** — real viscous CFD in SimScale gives more accurate drag

---

## 7. Bonus Task — Design Optimization

### 7.1 Problem Statement

Can we improve the fin design? Reduce stress while keeping drag and mass reasonable?

### 7.2 Optimization Strategy

| Parameter | Original | Optimized | Reason |
|-----------|----------|-----------|--------|
| Root chord | 150 mm | 140 mm | Less aggressive taper → lower bending moment |
| Tip chord | 75 mm | 70 mm | Proportional reduction |
| Thickness | 4.0 mm | 4.5 mm | More material at root → higher I → lower stress |

**Engineering logic:**
- Bending stress depends on moment (M) and section stiffness (I = chord × thickness³/12)
- Increasing thickness has a **cubic effect** on stiffness — very powerful
- Slightly reducing chord taper lowers the aerodynamic load distribution at root

### 7.3 How I Executed the Optimization

**Step 1 — Reused FEM and CFD solvers for both designs**

**Step 2 — Ran side-by-side comparison:**

| Metric | Original | Optimized | Change |
|--------|----------|-----------|--------|
| Max root stress (MPa) | 7.552 | 5.967 | **−21.0%** ✅ |
| Tip deflection (mm) | 0.147 | 0.104 | −29.8% ✅ |
| Factor of Safety | 36.54 | 46.25 | +26.5% ✅ |
| Drag coefficient Cd | 0.0106 | 0.0109 | +2.8% ⚠️ |
| Drag per span (N/m) | 7.301 | 7.004 | −4.1% ✅ |
| Mass (g) | 121.5 | 127.6 | +5.0% ⚠️ |

**Step 3 — Generated outputs:**
- `optimization_comparison.png` — bar chart comparing both designs
- `optimization_comparison.txt` — numerical comparison table

### 7.4 Optimization Conclusion

The optimized design is **better overall** for structural performance:
- **21% less stress** at the root (most critical location)
- **29% less deflection** (stiffer fin)
- **Higher safety margin** (FoS 36.5 → 46.3)
- Small trade-offs: 2.8% more drag coefficient, 5% more mass

For a rocket fin, **structural safety is paramount** — the small mass/drag increase is acceptable.

---

## 8. Files Created

| File | Purpose | Outputs Generated |
|------|---------|---------------------|
| `fem_fin_analysis.py` | FEM beam analysis + mesh convergence | `fem_mesh_convergence.png`, `fem_stress_distribution.png`, `fem_results_summary.txt` |
| `cfd_fin_panel_method.py` | Inviscid panel method CFD | `cfd_pressure_distribution.png`, `cfd_streamlines.png`, `cfd_results_summary.txt` |
| `bonus_design_optimization.py` | Original vs optimized comparison | `optimization_comparison.png`, `optimization_comparison.txt` |

---

## 9. How to Run

```bash
cd Rocketry_Project

# FEM structural analysis
python fem_fin_analysis.py

# CFD aerodynamic analysis
python cfd_fin_panel_method.py

# Design optimization comparison
python bonus_design_optimization.py
```

**Requirements:**
```bash
pip install numpy matplotlib
```

After running, check the generated `.png` plots and `.txt` summary files in the same folder.

---

## 10. Key Engineering Equations Used

### Structural (FEM)

| Equation | Purpose |
|----------|---------|
| q = ½ρV² | Dynamic pressure |
| w(x) = q × chord(x) | Distributed aerodynamic load |
| I = b×t³/12 | Second moment of area (rectangular section) |
| M = EI × d²v/dx² | Bending moment from curvature |
| σ = M×y/I | Bending stress |
| FoS = σ_yield/σ_max | Factor of safety |

### Aerodynamic (CFD)

| Equation | Purpose |
|----------|---------|
| Re = V×c/ν | Reynolds number |
| Cp = 1 − (V/V∞)² | Pressure coefficient |
| Cf = 0.074/Re^0.2 | Turbulent skin friction |
| Cd = Cf × FF × 2 | Total drag coefficient |
| D = Cd × q × c | Drag force per unit span |

---

## 11. Limitations and Notes

| Limitation | Explanation | Solution |
|------------|-------------|----------|
| 1D beam FEM (not 3D) | Simplified structural model | Full 3D FEM in SimScale |
| Inviscid panel method | No friction, separation, wake | Viscous RANS CFD in SimScale |
| Empirical drag estimate | Approximate Cd calculation | SimScale CFD for accurate drag |
| Uniform thickness | Real fins may vary thickness | SimScale allows complex geometry |
| Static load only | No vibration/flutter analysis | Advanced analysis beyond scope |

These Python scripts are **independent engineering checks** that demonstrate understanding of the physics and methods. SimScale provides the production-grade analysis required for final submission.

---

## 12. Conclusion

This rocketry project demonstrates:

1. **Structural analysis (FEM):** The original fin is structurally safe with FoS = 36.54 at 100 m/s. Maximum stress (7.55 MPa) is far below yield strength (276 MPa).

2. **Aerodynamic analysis (CFD):** The thin biconvex profile produces low drag (Cd ≈ 0.0106). Pressure distribution shows expected acceleration over the thickest section.

3. **Design optimization:** A modest geometry change (slightly less taper, slightly more thickness) reduces root stress by 21% with acceptable mass/drag trade-offs.

4. **Mesh convergence:** Results converge with 64 elements, validating the FEM approach.

These analyses form the foundation for the full SimScale simulations and demonstrate core aerospace engineering principles: **structures, aerodynamics, and design trade-offs**.

---

*See also: [`Rocketry_Project/`](Rocketry_Project/) for all source files and result summaries.*
